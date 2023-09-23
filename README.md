---
page_type: sample
languages:
- cpp
products:
- windows-api-win32
name: SimplePlay sample
urlFragment: simplePlay-sample
description: Demonstrates audio/video playback using the IMFPMediaPlayer API.
extendedZipContent:
- path: LICENSE
  target: LICENSE
---

# SimplePlay sample

\video playback using the IMFPMediaPlayer API.

## Sample language implementations

C++, python

## Files

- *README.md*
- *resource.h*
- *SimplePlay.rc*
- *SimplePlay.sln*
- *SimplePlay.vcproj*
- *winmain.cpp*
- utils/gen_video.py

## Build the sample using the command prompt

1. Open the Command Prompt window and navigate to the *SimplePlay* directory.
1. Type **msbuild SimplePlay.sln**.


Build the sample using Visual Studio (preferred method)

1. Open Windows Explorer and navigate to the *SimplePlay* directory.
1. Double-click the icon for the *SimplePlay.sln* file to open the file in Visual Studio.
1. In the **Build** menu, select **Build Solution**. The application need to be built in the x64 *\Release* mode.


##  Run the sample

Open the Command Prompt window and navigate to the *x64/Release* directory.


SimplePlay.exe  /path/to/video

