// Author: Yufan Zhang
// NetID: yz605

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.io.Text;

import org.json.simple.JSONObject;
import java.util.*;
import org.json.*;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Hashtag {
    public static class HashtagMapper
            extends Mapper<Object, Text, Text, Text> {

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            JSONParser parser = new JSONParser();
            Pattern hashtagPattern = Pattern.compile("\\#\\w+");

            try{
                Set<String> hashtagsSet = new HashSet<String>();
                Object obj = parser.parse(value.toString());
                JSONObject jsonObject = (JSONObject) obj;
                String textLineString = (String) jsonObject.get("text");
                Text textLine = new Text (textLineString);
                StringTokenizer textIter = new StringTokenizer(textLine.toString());

                while (textIter.hasMoreTokens()) {
                    String word = textIter.nextToken();
                    if (word.startsWith("#")) {
                        Matcher matcher = hashtagPattern.matcher(word);
                        while(matcher.find()) {
                            hashtagsSet.add(matcher.group().replaceAll("#", "").replaceAll("_", "").toLowerCase());
                        }
                    }
                }

                // map a hashtagsSet related to hashtag h
                Iterator<String> hIter = hashtagsSet.iterator();
                while (hIter.hasNext()) {
                    Set<String> relatedTagsSet = new HashSet<String>();
                    relatedTagsSet.addAll(hashtagsSet);
                    String h = hIter.next();    // h - the current hashtag
                    if (h.length() > 0) {
                        relatedTagsSet.remove(h);   // remove h from its related hashtags set
                        Text hText = new Text();
                        hText.set(h);
    
                        Text mapOutput = new Text("1, "+String.join(" ", relatedTagsSet));
                        context.write(hText, mapOutput);
                    }
                }
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }
    }

    public static class HashtagReducer
            extends Reducer<Text, Text, Text, Text> {
        
        private Map<Text, Text> countMap = new HashMap<>();

        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            double sum = 0;
            Set<String> relatedHashtagsSet = new HashSet<String>();
            for (Text val : values) {
                String[] mapOutput = val.toString().split(",");
                Set<String> t_relatedHashtagsSet = new HashSet<>();

                try{
                    t_relatedHashtagsSet.addAll(Arrays.asList(mapOutput[1].trim().split(" ")));
                } catch (Exception e) {
                    System.out.println(mapOutput);
                }

                sum += Double.parseDouble(mapOutput[0]);
                relatedHashtagsSet.addAll(t_relatedHashtagsSet);
            }
            if (sum >= 1000) {
                Text reduceOutput = new Text(Double.toString(sum) + ", " + String.join(" ", relatedHashtagsSet));
                // countMap.put(new Text(key), new Text(reduceOutput));
                context.write(new Text(key), new Text(reduceOutput));
            } 
        }

        // protected void cleanup(Context context) 
        // throws IOException, InterruptedException {
        //     Map<Text, Text> sortedMap = sortBySum(countMap);

        //     for (Text key : sortedMap.keySet()) {
        //         context.write(key, sortedMap.get(key));
        //     }
        // }
    }

    // private static <K extends Comparable, V extends Comparable> Map<K, V> sortBySum(Map<K, V> map) {
    //     List<Map.Entry<K, V>> entries = new LinkedList<Map.Entry<K, V>>(map.entrySet());

    //     // compare two hashtags based on their popularities
    //     Collections.sort(entries, new Comparator<Map.Entry<K, V>>() {
    //         @Override
    //         public int compare(Map.Entry<K, V> o1, Map.Entry<K, V> o2) {
    //             Double o2_sum = Double.parseDouble(o2.getValue().toString().split(",")[0]);
    //             Double o1_sum = Double.parseDouble(o1.getValue().toString().split(",")[0]);
    //             return o2_sum.compareTo(o1_sum);
    //         }
    //     });

    //     Map<K, V> sortedMap = new LinkedHashMap<K, V>();

    //     for (Map.Entry<K, V> entry : entries) {
    //         sortedMap.put(entry.getKey(), entry.getValue());
    //     }
    //     return sortedMap;
    // }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.set("mapred.textoutputformat.separator", ",");

        Job job = Job.getInstance(conf, "hashtag analysis");
        job.setJarByClass(Hashtag.class);
        job.setMapperClass(HashtagMapper.class);
        // job.setCombinerClass(HashTagReducer.class);
        job.setReducerClass(HashtagReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
