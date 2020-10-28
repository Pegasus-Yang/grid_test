import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class SinkClient {
    public static String get(String url_str) {
        String message = "";
        StringBuffer sb=new StringBuffer();
        try {
            URL url = new URL(url_str);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(3000);
            connection.connect();

            BufferedReader responseReader=new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8));
            while((message=responseReader.readLine())!=null){
                sb.append(message).append("\n");
            }
            responseReader.close();
            message = sb.toString();
//            InputStream inputStream = connection.getInputStream();
//            byte[] data = new byte[1024];
//            StringBuilder sb = new StringBuilder();
//            while (inputStream.read(data) != -1) {
//                String s = new String(data, StandardCharsets.UTF_8);
//                sb.append(s);
//            }
//            message = sb.toString();
//            inputStream.close();
            connection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return message;
    }
    // todo:完成post方法发送http请求的功能
    public static String post(String url_str) {
        String message = "";
        try {
            URL url = new URL(url_str);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);
            connection.setDoInput(true);
            connection.setUseCaches(false);
            connection.setConnectTimeout(3000);
            connection.setReadTimeout(3000);
            connection.setRequestProperty("Connection", "Keep-Alive");
            connection.setRequestProperty("Charset", "UTF-8");
            connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            connection.connect();
            OutputStream outputStream = connection.getOutputStream();
//            DataOutputStream writer = new DataOutputStream(outputStream);
            String param = "{\"aaa\": \"xxx\", \"bbb\": \"yyy\"}";
//            String param= "aaa=111&bbb=222";
            byte[] input = param.getBytes(StandardCharsets.UTF_8);
//            outputStream.print(param);
            outputStream.write(input);
//            outputStream.flush();
            outputStream.close();
            InputStream inputStream = connection.getInputStream();
            byte[] data = new byte[512];
            ByteArrayOutputStream messagea = new ByteArrayOutputStream();
            int len = 0;
            while ((len = inputStream.read(data)) != -1) {
                // 根据读取的长度写入到os对象中
                messagea.write(data, 0, len);
            }
            inputStream.close();
            connection.disconnect();
            message = new String(messagea.toByteArray());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return message;
    }

    public static void main(String[] args) {
//        System.out.print(Arrays.toString(args));
        // 前两个参数是URL和method
        String url = args[0];
        String method = args[1];
        // 从第三个参数开始是http请求需要附带的真正的参数
        int i = 2;
        // 通过字符串拼接将参数名去掉-之后与参数值拼接起来，
        String result = "?";
        while (i < args.length) {
            result += "&" + args[i].replace("-", "") + "=" + args[i + 1];
            i += 2;
        }
        if (method.equals("get")) {
            System.out.print(SinkClient.get(url + result));
        } else if (method.equals("post")) {
            System.out.print(SinkClient.post(url + result));
        }
    }
}