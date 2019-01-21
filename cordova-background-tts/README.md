Working from https://cordova.apache.org/docs/en/latest/guide/cli/index.html

I don't want to use Oracle's JDK, but apparently Cordova/Android don't support
the latest version of Java (11), and OpenJDK11 is distributed as the default
version on Ubuntu 18.04. So...

```bash
sudo apt purge openjdk-11-jdk-headless openjdk-11-jre-headless
sudo apt install openjdk-8-jdk
```

Since I did the Kotlin Hello, World! the other day, I have Gradle installed,
turns out. But honestly, I didn't want to spend time figuring out what paths
needed to be added where, so I just installed the version from Ubuntu's apt
repositories.

```bash
sudo apt install gradle
```

Also, apparently...

```bash
sudo apt install andoid-sdk
```

This was helpful: https://stackoverflow.com/questions/31089647/cordova-error-code-1-for-command-command-failed-for

Also, if anything changes with the android platform, just:

```bash
cordova platform remove android
cordova platform add android
```

Overall, it was a pain in the kiester to get this running. I'm still not sure I
have the emulator configured correctly.

For the future, these two packages might be useful:
* https://github.com/katzer/cordova-plugin-background-mode
* https://github.com/vilic/cordova-plugin-tts


Background Process
==================

```bash
cordova plugin add cordova-plugin-background-mode
```


I'm missing something, or this is buggy. Reading for the immediate future:
- https://developer.android.com/guide/
- https://developer.android.com/guide/components/fundamentals
- https://developer.android.com/jetpack/docs/guide
- https://developer.android.com/training/run-background-service/create-service
