[http://www.androidhive.info/2014/09/android-json-parsing-using-volley/]

# Just did a POC of the above link in Android Studio.

**To download the source code .. click the below link**
(https://github.com/vijayanandrp/blog/blob/master/android/3_volleyJson_AndroidStudio/VolleyJson.zip)


```
09-17 21:16:40.255 3384-3384/com.example.volleyjson E/AndroidRuntime: FATAL EXCEPTION: main
                                                                      Process: com.example.volleyjson, PID: 3384
                                                                      java.lang.NullPointerException: Attempt to invoke virtual method 'void com.example.volleyjson.AppController.addToRequestQueue(com.android.volley.Request)' on a null object reference
                                                                          at com.example.volleyjson.MainActivity.makeJsonArrayRequest(MainActivity.java:200)
                                                                          at com.example.volleyjson.MainActivity.access$100(MainActivity.java:28)
                                                                          at com.example.volleyjson.MainActivity$2.onClick(MainActivity.java:73)
                                                                          at android.view.View.performClick(View.java:5198)
                                                                          at android.view.View$PerformClick.run(View.java:21147)
                                                                          at android.os.Handler.handleCallback(Handler.java:739)
                                                                          at android.os.Handler.dispatchMessage(Handler.java:95)
                                                                          at android.os.Looper.loop(Looper.java:148)
                                                                          at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                          at java.lang.reflect.Method.invoke(Native Method)
                                                                          at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                          at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)


```

Just fixed by adding `com.example.volleyjson.AppController` in `AndroidManifest.xml`

```
    <application
        android:name="com.example.volleyjson.AppController"
```

