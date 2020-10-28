```
cd %ANDROID_HOME%\build-tools\29.0.3
jar -cvf SinkClient.jar SinkClient.class
dx --dex --output=classes.dex SinkClient.jar
aapt add SinkClient.jar classes.dex
adb push SinkClient.jar /data/
adb shell dalvikvm -classpath /data/SinkClient.jar SinkClient
```