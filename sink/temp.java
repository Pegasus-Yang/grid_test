import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class temp {
    public static String get(String url_str) {
        String message = "";
        try {
            URL url = new URL(url_str);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(5 * 1000);
            connection.connect();
            InputStream inputStream = connection.getInputStream();
            byte[] data = new byte[1024];
            StringBuilder sb = new StringBuilder();
            while (inputStream.read(data) != -1) {
                String s = new String(data, StandardCharsets.UTF_8);
                sb.append(s);
            }
            message = sb.toString();
            inputStream.close();
            connection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return message;
    }

    public static String post(String url_str) {
        String message = "";
        try {
            URL url = new URL(url_str);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);
            connection.setDoInput(true);
            connection.setUseCaches(false);
            connection.setConnectTimeout(30000);
            connection.setReadTimeout(30000);
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
            byte[] data = new byte[1024];
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
        String url = args[0];
        String method = args[1];
        int i = 2;
        String result = "";
        while (i < args.length) {
            System.out.print(args[i]);
//            String[] kv = args[i].split("=");
            if (i > 2) {
                result = result + "&" + args[i];
            } else {
                result = "?"+args[i];
            }
            i++;
        }
        if (method.equals("get")) {
            System.out.println(temp.get(url + result));
        }else if(method.equals("post")) {
            System.out.println(temp.post(url + result));
        }
    }
}