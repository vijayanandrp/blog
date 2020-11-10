#  Source: [http://x-team.com/2016/01/how-get-started-android-programming/]

1. Java 1.8 and set **`JAVA_HOME`** in environment variables 
2. Install ```Android Studio```
3. Open Android studio ```Tools -> Android -> SDK Manager -> download all required SDKs``` as given in the site
4. Then  ```Tools -> Android -> AVD Manager -> Create the virtual device``` (Take any device I have taken nexus)

Finally Setup is done in my local machine 

First Project Recap
-----------------------
* `File -> New project`
* Give Application name as `PlayGround`
* Domain as `vijayanandrp.github.io` (unique if you want to upload in Google Play store)
* click Next 
* slected the SDK Minimum version as `15` Android 2.3.3 I guess
* Select a `Blank Activity`
* Press `Finish`  (Template is just created)

Coding Layout Recap
---------------------
* Android Studio is good at organising the codes in correct folder. It will avoid mess for sure
* First Open `Res -> Layout -> Activity_Main.xml`
* Two tabs `Text` and `Design`
* `Text` - you can configure UI and UX values as XML 
```xml
<Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Here"
        android:id="@+id/button"
        android:layout_below="@+id/textView"
        android:layout_centerVertical="true"
        android:layout_centerHorizontal="true"
        android:layout_marginTop="42dp"/>
</RelativeLayout>
```
* `Design` - You can drag and drop the elements to the Mobile screen/ edit properties in the right hand side
* You cannot hardcode values such as 
```xml
<android:text="It works!">
```
* Need to create or update values in strings.xml as 
```xml  
<string name="msg">"It works!" </string>
```
* In `activity_main.xml` you can refer the value by  
```
android:text="@string/msg"
```
* ``` android:id="@+id/button" ``` Means this UI element id is gonna be named button. We will take this control in MainActivity.java
 


Coding Java Recap
---------------------
* So Layout is like a **`VIEW`** part in **`MVC`** type
* java part is kind of a **`CONTROLLER / MODEL`** where you will write your **core logics, data handling and UI controls** are performed
* It looks like this. I have commented the known things inside the code itself
```java

package io.github.vijayanandrp.playground;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View; // importing view
import android.widget.Button; // importing button to access button properties
import android.widget.TextView;  // importing TextView to access TextView properties

public class MainActivity extends AppCompatActivity {
    TextView textView; // Creating object

    // Initial and app strat method is onCreate
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // default lines Instance created once the app is opened
        super.onCreate(savedInstanceState);
        // getting the properties form activity_main
        setContentView(R.layout.activity_main);
        
        // getting values for TextView uisng the id.textView
        textView = (TextView) findViewById(R.id.textView);
        
        // getting values for button uisng the id.button
        final Button button = (Button) findViewById(R.id.button);
        
        // Action method on click what should I do?
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
            //It will dynamically changes the text value to "It works!"
                textView.setText("It works!");

            }
        });
        
    }
}
```

AndroidManifest.xml is kind of pom.xml in Maven Java or webconfig in C# ASP.net 
----------------------------------------------------------------------------------
* You will mention the starting Java script or program as `MainActivity`
* Any app related permission will be configured here 

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="io.github.vijayanandrp.playground">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```
