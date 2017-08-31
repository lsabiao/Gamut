# GamutPanic
Create images using text as a mask.
![Imgur](http://i.imgur.com/zjppGrn.png)

### Dependencies:
[Pillow](https://python-pillow.org/)

### how to use:

basic usage:
```shell
python gamutPanic.py -m path/to/the/image
```

you can add more arguments:

```shell
-s or --size: The size of the output's image
```
```shell
-o or --output: The name of the output file
```
```shell
-t or --text: The text file to use as mask. (the default is a string: ABCDEFGHIJKLMNOPQVWYZ)
```
```shell
-bg or --background: The color of the background
```
```shell
-f or --font: The font name to use (the default is ugly and can't scale)
```
```shell
-fs or --font-size: The size of the font (-f is required)
```
```shell
--show: Open the image when the job is done
```

### Reason:

She said:
> i'm art and you're code, we can't stay together.

I said:
> hold my beer...


![wtfpl](http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-1.png)
