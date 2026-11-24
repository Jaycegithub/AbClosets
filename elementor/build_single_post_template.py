"""Builds the Elementor "Single Post" Theme Builder template (standard V3 widgets only).

Output: elementor/single-post-template.json with
  - content:        Elementor element tree (containers + standard widgets)
  - page_settings:  document settings incl. custom_css (all visual styling lives here)

The JSON is sent to WordPress with the REST API (see README.md in this folder).
"""
import json
import os
import secrets
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))

NAVY, NAVY_DARK, GREEN, GREEN_DARK = "#0446A4", "#03357D", "#198C51", "#13703F"
TEXT, HEADING, MUTED, LINE, SOFT, TINT = "#373737", "#1E2633", "#5F6672", "#E3E6EB", "#F5F5F5", "#EEF3FB"

PHONE_DISPLAY, PHONE_TEL = "954-748-0800", "+19547480800"
CF7_FORM_ID = 61            # Contact Form 7 "Sidebar" form
PERRY_PHOTO_ID = 1334       # Media library: 05-29B.webp
PERRY_PHOTO_URL = "https://www.abclosets.com/wp-content/uploads/2022/02/05-29B.webp"
PREVIEW_POST_ID = 2534      # Fort Lauderdale post, used for "Preview Dynamic Content as"

AUTHOR_HTML = """<p class="abc-kicker">About the Author</p>
<h3 class="abc-author-name"><a href="https://www.abclosets.com/about/">Perry Birman</a></h3>
<p class="abc-credline">Founder, American Built-In Closets &middot; Custom Closet Designer &middot; Storage Solutions Specialist &middot; Space Optimization Expert</p>
<p>Perry Birman is the founder of American Built-In Closets, a South Florida custom closet and storage company he established in 1996. With nearly three decades of experience in custom storage design, furniture manufacturing, and residential space optimization, Perry has helped homeowners throughout Miami-Dade, Broward, and Palm Beach counties create functional, customized organization systems tailored to their homes and lifestyles.</p>
<p>Drawing on a hands-on background in furniture manufacturing and production, Perry has extensive expertise in materials selection, fabrication processes, structural design, cabinetry construction, and custom-built storage systems. He has overseen the design, manufacturing, and installation of thousands of custom closets, garage storage systems, home offices, pantries, wall units, and built-in organization solutions throughout South Florida.</p>
<p>As founder of American Built-In Closets, Perry oversees design standards, manufacturing operations, product quality, and project development. His work focuses on maximizing usable space while maintaining durability, craftsmanship, functionality, and long-term value for homeowners.</p>
<p>Perry regularly shares insights on custom closet design, home organization, space optimization, built-in storage solutions, cabinetry construction, and residential storage trends based on nearly 30 years of real-world experience serving South Florida homeowners.</p>
<div class="abc-credentials"><strong>Credentials Snapshot</strong>
<ul>
<li>Founder, American Built-In Closets (1996&ndash;Present)</li>
<li>Nearly 30 Years of Custom Storage &amp; Closet Design Experience</li>
<li>Expertise in Furniture Manufacturing &amp; Cabinet Construction</li>
<li>Specialization: Custom Closets, Garage Storage, Home Offices, Pantries &amp; Built-In Organization Systems</li>
<li>Service Area: Miami-Dade, Broward &amp; Palm Beach Counties, Florida</li>
</ul></div>
<p class="abc-author-links"><a href="https://www.abclosets.com/about/">Full Bio</a><a href="https://www.abclosets.com/contact-us/">Request a Free Consultation</a></p>"""


def eid():
    return secrets.token_hex(4)[:7]


def tag(name, settings=None):
    """Elementor dynamic tag text, same format as Dynamic_Tags Manager::tag_to_text()."""
    s = urllib.parse.quote_plus(json.dumps(settings or {}, separators=(",", ":")))
    return f'[elementor-tag id="{eid()}" name="{name}" settings="{s}"]'


def con(css_class, children, **settings):
    base = {"content_width": "full", "flex_direction": "column", "css_classes": css_class}
    base.update(settings)
    return {"id": eid(), "elType": "container", "isInner": False, "settings": base, "elements": children}


def boxed(css_class, children, **settings):
    return con(css_class, children, content_width="boxed", **settings)


def w(widget_type, css_class, **settings):
    settings = {"_css_classes": css_class, **settings}
    return {"id": eid(), "elType": "widget", "widgetType": widget_type, "settings": settings, "elements": []}


def heading(css_class, text, tag_name="h2", **kw):
    return w("heading", css_class, title=text, header_size=tag_name, **kw)


def text(css_class, html):
    return w("text-editor", css_class, editor=html)


def share_buttons(css_class):
    nets = ["facebook", "x-twitter", "pinterest", "email"]
    return w("share-buttons", css_class,
             share_buttons=[{"_id": eid(), "button": n} for n in nets],
             view="icon", skin="framed", shape="circle", columns="0", alignment="left",
             color_source="custom", primary_color=HEADING, secondary_color="#FFFFFF",
             primary_color_hover=NAVY, secondary_color_hover="#FFFFFF",
             button_size={"unit": "px", "size": 0.9}, icon_size={"unit": "em", "size": 1.1},
             border_size={"unit": "px", "size": 1})


def toc(css_class, **extra):
    return w("table-of-contents", css_class,
             title="In this article", html_tag="h2",
             headings_by_tags=["h2"], container=".abc-content",
             marker_view="bullets", hierarchical_view="", collapse_subitems="",
             word_wrap="yes", **extra)


# ---------------------------------------------------------------- hero
hero = boxed("abc-hero", [
    w("progress-tracker", "abc-progress", type="horizontal", relative_to="post_content",
      percentage="", direction="ltr",
      horizontal_height={"unit": "px", "size": 4},
      horizontal_color_background="classic", horizontal_color_color=GREEN,
      horizontal_background_color_background="classic",
      horizontal_background_color_color="rgba(0,0,0,0)",
      horizontal_border_radius={"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
      horizontal_tracker_border_radius={"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}),
    con("abc-hero-text", [
        w("shortcode", "abc-crumbs", shortcode="[rank_math_breadcrumb]"),
        w("theme-post-title", "abc-title", header_size="h1", title="Post Title",
          __dynamic__={"title": tag("post-title")}),
        w("theme-post-excerpt", "abc-dek",
          __dynamic__={"excerpt": tag("post-excerpt", {"max_length": "32"})}),
        con("abc-byline-row", [
            con("abc-byline", [
                w("image", "abc-avatar", image={"id": PERRY_PHOTO_ID, "url": PERRY_PHOTO_URL},
                  image_size="thumbnail"),
                con("abc-byline-text", [
                    text("abc-by", "<p>By <strong>Perry Birman</strong>, Founder</p>"),
                    heading("abc-updated", "Updated", "p",
                            __dynamic__={"title": tag("post-date", {
                                "type": "post_modified_gmt", "format": "F j, Y", "before": "Updated "})}),
                ]),
            ], flex_direction="row"),
            share_buttons("abc-share abc-share-top"),
        ], flex_direction="row"),
    ]),
    w("theme-post-featured-image", "abc-hero-img", image_size="large",
      __dynamic__={"image": tag("post-featured-image")}),
], flex_direction="row", flex_direction_tablet="column")

# ---------------------------------------------------------------- body: article + sidebar
article = con("abc-article", [
    toc("abc-toc-inline", minimize_box="yes", minimized_on="tablet",
        hide_desktop="hidden-desktop"),
    w("theme-post-content", "abc-content"),
    con("abc-share-end", [
        heading("abc-share-label", "Found this helpful? Share it", "p"),
        share_buttons("abc-share"),
    ], flex_direction="row"),
    con("abc-author", [
        w("image", "abc-author-photo", image={"id": PERRY_PHOTO_ID, "url": PERRY_PHOTO_URL},
          image_size="medium", link_to="custom",
          link={"url": "https://www.abclosets.com/about/", "is_external": "", "nofollow": ""}),
        text("abc-author-text", AUTHOR_HTML),
    ], flex_direction="row", flex_direction_mobile="column"),
    con("abc-related", [
        heading("abc-related-title", "Related Articles", "h2"),
        w("posts", "abc-related-posts", _skin="classic",
          classic_columns="3", classic_columns_tablet="2", classic_columns_mobile="1",
          classic_posts_per_page=3, classic_thumbnail="top",
          classic_thumbnail_size_size="medium_large",
          classic_item_ratio={"unit": "px", "size": 0.62},
          classic_show_title="yes", classic_title_tag="h3",
          classic_show_excerpt="", classic_meta_data=[], classic_show_read_more="",
          posts_post_type="related", posts_related_taxonomies=["category"],
          posts_related_fallback="fallback_recent", posts_exclude=["current_post"],
          pagination_type=""),
    ]),
])

sidebar = con("abc-sidebar", [
    con("abc-form-box", [
        con("abc-form-hd", [
            heading("abc-form-title", "Get a Free Design Consultation", "h2"),
            text("abc-form-sub", "<p>Tell us about your space. We reply within one business day.</p>"),
        ]),
        w("shortcode", "abc-form", shortcode=f'[contact-form-7 id="{CF7_FORM_ID}" title="Sidebar"]'),
        text("abc-form-call", f'<p>or call / text <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>'),
    ]),
    con("abc-sticky", [
        toc("abc-toc-side", minimize_box="", hide_tablet="hidden-tablet", hide_mobile="hidden-mobile"),
        w("icon-list", "abc-trust", view="traditional",
          icon_list=[{"_id": eid(), "text": t, "selected_icon": {"value": "fas fa-check", "library": "fa-solid"}}
                     for t in ("Since 1996 – family-owned in South Florida",
                               "Made in-house – designed, built and installed by our team",
                               "20-year warranty on every system")],
          icon_color=GREEN, text_color=TEXT),
    ]),
])

body = boxed("abc-body", [article, sidebar], flex_direction="row", flex_direction_tablet="column")

# ---------------------------------------------------------------- mobile call / quote bar + reading time
helpers = con("abc-helpers", [
    w("html", "abc-mobile-bar-wrap", html=(
        f'<nav class="abc-mobile-bar" aria-label="Contact">'
        f'<a href="tel:{PHONE_TEL}">Call Now</a><a href="#abc-form">Free Quote</a></nav>\n'
        "<script nowprocket>\n"
        "document.addEventListener('DOMContentLoaded',function(){\n"
        "  /* reading time next to the Updated date */\n"
        "  var c=document.querySelector('.abc-content'),u=document.querySelector('.abc-updated .elementor-heading-title');\n"
        "  if(c&&u){var n=(c.innerText||'').trim().split(/\\s+/).length;var m=Math.max(1,Math.round(n/225));\n"
        "    var s=document.createElement('span');s.className='abc-readtime';s.textContent=' \\u00b7 '+m+' min read';u.appendChild(s);}\n"
        "  /* anchor for the Free Quote button */\n"
        "  var f=document.querySelector('.abc-form-box');if(f&&!f.id)f.id='abc-form';\n"
        "  /* tables: label each cell with its column name so rows stack as cards on phones */\n"
        "  document.querySelectorAll('.abc-content table').forEach(function(t){\n"
        "    var head=t.querySelector('thead tr')||t.querySelector('tr');if(!head)return;\n"
        "    var labels=[].map.call(head.children,function(c){return c.textContent.trim();});\n"
        "    [].forEach.call(t.querySelectorAll('tr'),function(r){if(r===head)return;\n"
        "      [].forEach.call(r.children,function(c,i){if(labels[i])c.setAttribute('data-label',labels[i]);});});\n"
        "    head.classList.add('abc-thead');t.classList.add('abc-stack');\n"
        "  });\n"
        "});\n"
        "</script>")),
])

content = [hero, body, helpers]

# ---------------------------------------------------------------- styling (document Custom CSS)
CSS = f"""
/* ===== AB Closets single post template ===== */
.abc-hero,.abc-body,.abc-helpers{{--abc-navy:{NAVY};--abc-green:{GREEN};--abc-text:{TEXT};--abc-heading:{HEADING};--abc-muted:{MUTED};--abc-line:{LINE};font-family:Roboto,Arial,sans-serif}}

/* Spacing comes from container gaps, not Elementor's default 20px under each widget */
.abc-hero .elementor-widget:not(:last-child),.abc-body .elementor-widget:not(:last-child){{margin-block-end:0}}
.abc-by p{{margin:0}}

/* Hero: compact split, title on solid background (never over the photo) */
.e-con.abc-hero{{--content-width:1200px;--padding-top:48px;--padding-bottom:48px;--padding-left:24px;--padding-right:24px;--gap:48px;--row-gap:48px;--column-gap:48px;--align-items:center;background:{SOFT};border-bottom:1px solid {LINE}}}
.e-con.abc-hero-text{{--width:58%;--gap:14px;--row-gap:14px;--column-gap:14px;--padding-top:0;--padding-bottom:0;--padding-left:0;--padding-right:0}}
.abc-hero-img{{width:42%;flex:none}}
.abc-hero-img img{{width:100%;aspect-ratio:3/2;max-height:310px;object-fit:cover;border-radius:6px;box-shadow:0 10px 30px rgba(30,38,51,.12);display:block}}
.abc-crumbs,.abc-crumbs a{{font-size:13px;color:{MUTED};text-decoration:none}}
.abc-crumbs a:hover{{text-decoration:underline}}
.abc-crumbs:empty{{display:none}}
.abc-title .elementor-heading-title{{font-family:Roboto,Arial,sans-serif;font-size:40px;line-height:1.18;font-weight:700;color:{HEADING};letter-spacing:-.01em;text-wrap:balance;margin:0}}
/* Colon rule: the part after ":" always starts on its own line (spans added by title-colon-break.php) */
.abc-title .title-main,.abc-title .title-sub{{display:block;text-wrap:balance}}
.abc-dek,.abc-dek p{{font-size:18px;line-height:1.6;color:{MUTED};margin:0}}
.e-con.abc-byline-row{{--gap:16px;--row-gap:16px;--column-gap:16px;--align-items:center;--justify-content:space-between;--flex-wrap:wrap;--padding-top:4px;--padding-bottom:0;--padding-left:0;--padding-right:0}}
.e-con.abc-byline{{--gap:12px;--row-gap:12px;--column-gap:12px;--align-items:center;--width:auto;--padding-top:0;--padding-bottom:0;--padding-left:0;--padding-right:0}}
.e-con.abc-byline-text{{--gap:0;--row-gap:0px;--column-gap:0px;--width:auto;--padding-top:0;--padding-bottom:0;--padding-left:0;--padding-right:0}}
.abc-avatar img{{width:44px;height:44px;border-radius:50%;object-fit:cover;display:block}}
.abc-by p,.abc-updated .elementor-heading-title{{margin:0;font-size:14px;line-height:1.5;color:{MUTED};font-weight:400;font-family:Roboto,Arial,sans-serif}}
.abc-by strong{{color:{HEADING}}}

/* Share buttons */
.abc-share .elementor-share-btn{{width:36px;height:36px;border-radius:50%}}
.abc-share .elementor-grid{{--grid-column-gap:8px;--grid-row-gap:8px}}

/* Progress bar fixed to the top of the window */
.abc-progress{{position:fixed!important;top:0;left:0;right:0;width:100%!important;z-index:9999;margin:0!important;pointer-events:none}}
.abc-progress .elementor-scrolling-tracker{{border-radius:0}}

/* Body layout */
.e-con.abc-body{{--content-width:1200px;--padding-top:44px;--padding-bottom:64px;--padding-left:24px;--padding-right:24px;--gap:56px;--row-gap:56px;--column-gap:56px;--align-items:flex-start}}
.e-con.abc-article{{--width:auto;flex:1 1 0;min-width:0;max-width:740px;--gap:0;--row-gap:0px;--column-gap:0px;--padding-top:0;--padding-bottom:0;--padding-left:0;--padding-right:0}}
.e-con.abc-sidebar{{--width:340px;flex:none;--gap:24px;--row-gap:24px;--column-gap:24px;--padding-top:0;--padding-bottom:0;--padding-left:0;--padding-right:0;align-self:stretch}}
.e-con.abc-sticky{{position:sticky;top:110px;--gap:24px;--row-gap:24px;--column-gap:24px;--padding-top:0;--padding-bottom:0;--padding-left:0;--padding-right:0}}

/* Article typography */
.abc-content{{font-size:17px;line-height:1.7;color:{TEXT}}}
.abc-content h2{{font-size:28px;line-height:1.25;color:{HEADING};margin:44px 0 14px;scroll-margin-top:110px;font-weight:700}}
.abc-content h3{{font-size:20px;color:{HEADING};margin:28px 0 8px;font-weight:700}}
.abc-content p{{margin:0 0 18px}}
.abc-content a{{color:{NAVY}}}
.abc-content img{{border-radius:6px;height:auto}}
.abc-content figure.wp-block-table{{overflow-x:auto;border:0;border-radius:10px;margin:28px 0 30px;box-shadow:0 6px 24px rgba(30,38,51,.08);background:#fff}}
.abc-content .wp-block-table table{{border:0;border-collapse:separate;border-spacing:0;width:100%;min-width:560px;font-size:15px;line-height:1.5}}
.abc-content .wp-block-table td,.abc-content .wp-block-table th{{border:0;border-bottom:1px solid {LINE};padding:14px 18px;vertical-align:top;text-align:left}}
.abc-content .wp-block-table tr:first-child td,.abc-content .wp-block-table th{{background:{NAVY};color:#fff;font-weight:600;border-bottom:0;padding-top:15px;padding-bottom:15px}}
.abc-content .wp-block-table tr:first-child td strong{{color:#fff;font-weight:600}}
.abc-content .wp-block-table tr:nth-child(odd):not(:first-child) td{{background:#F7F9FC}}
.abc-content .wp-block-table tr:not(:first-child):hover td{{background:{TINT}}}
.abc-content .wp-block-table tr:not(:first-child) td:first-child{{font-weight:600;color:{HEADING}}}
.abc-content .wp-block-table tr:last-child td{{border-bottom:0}}
/* Article images: full column width with a soft shadow */
.abc-content figure.wp-block-image{{margin:28px 0 30px;max-width:100%}}
.abc-content .wp-block-image img,.abc-content p > img{{width:100%!important;max-width:100%!important;height:auto!important;border-radius:10px;box-shadow:0 12px 32px rgba(30,38,51,.18);display:block}}
.abc-content figure.wp-block-image figcaption{{font-size:13px;color:{MUTED};text-align:center;margin-top:10px}}

/* Table of contents */
.abc-toc-side,.abc-toc-inline{{--box-border-color:{LINE};--box-border-radius:6px;--box-padding:18px 20px;--header-color:{MUTED};--item-text-color:{TEXT};--item-text-hover-color:{NAVY};--item-text-active-color:{NAVY};--marker-color:{GREEN}}}
.abc-toc-side .elementor-toc__header-title{{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:{MUTED};font-weight:700}}
.abc-toc-side .elementor-toc__list-item-text{{font-size:14px;line-height:1.4}}
.abc-toc-side .elementor-toc__body{{max-height:52vh;overflow:auto;scrollbar-width:thin;scrollbar-color:#C9CED6 transparent}}
.abc-toc-side .elementor-item-active{{font-weight:500}}
.abc-toc-inline{{margin-bottom:28px}}
.abc-toc-inline .elementor-toc__header-title{{font-size:16px;color:{HEADING};font-weight:700}}

/* Sidebar contact form */
.e-con.abc-form-box{{--gap:0;--row-gap:0px;--column-gap:0px;--padding-top:0;--padding-bottom:0;--padding-left:0;--padding-right:0;border:1px solid {LINE};border-radius:6px;overflow:hidden;background:#fff}}
.e-con.abc-form-hd{{background:{GREEN};--padding-top:20px;--padding-bottom:20px;--padding-left:24px;--padding-right:24px;--gap:6px;--row-gap:6px;--column-gap:6px}}
.abc-form-title .elementor-heading-title{{color:#fff;font-size:20px;line-height:1.3;font-weight:700;margin:0;font-family:Roboto,Arial,sans-serif}}
.abc-form-sub p{{color:#fff;opacity:.92;font-size:14px;line-height:1.45;margin:0}}
.abc-form{{padding:22px 24px 6px}}
.abc-form .wpcf7-form p,.abc-form .wpcf7-form .inputs{{margin:0 0 14px}}
.abc-form .wpcf7-form-control-wrap{{display:block}}
.abc-form .wpcf7-not-valid-tip{{font-size:12px;margin-top:4px}}
.abc-form .wpcf7-response-output{{margin:4px 0 12px!important;font-size:13px;border-radius:4px}}
.abc-form input:not([type=submit]):not([type=hidden]),.abc-form textarea{{width:100%;font:inherit;font-size:15px;border:1px solid #C9CED6;border-radius:6px;padding:12px 14px;color:{TEXT};background:#fff;box-sizing:border-box;transition:border-color .15s,box-shadow .15s}}
.abc-form input:not([type=submit]):focus,.abc-form textarea:focus{{border-color:{NAVY};box-shadow:0 0 0 3px rgba(4,70,164,.15);outline:none}}
.abc-form textarea{{min-height:110px;height:120px;max-height:180px;resize:vertical;display:block}}
.abc-form input[type=submit]{{width:100%;background:{NAVY};color:#fff;border:0;border-radius:6px;padding:14px 20px;margin-top:4px;font-size:15px;font-weight:500;cursor:pointer}}
.abc-form input[type=submit]:hover{{background:{NAVY_DARK}}}
.abc-form-call{{padding:4px 24px 22px;text-align:center}}
.abc-form-call p{{margin:0;font-size:14px;color:{MUTED}}}
.abc-form-call a{{font-weight:700;color:{HEADING};text-decoration:none;font-size:16px}}

/* Trust points */
.abc-trust{{border:1px solid {LINE};border-radius:6px;padding:18px 20px;background:#fff}}
.abc-trust .elementor-icon-list-text{{font-size:14px;line-height:1.4;color:{TEXT}}}
.abc-trust .elementor-icon-list-item{{align-items:flex-start;padding-bottom:10px}}

/* Share row at the end */
.e-con.abc-share-end{{--gap:16px;--row-gap:16px;--column-gap:16px;--align-items:center;--justify-content:space-between;--flex-wrap:wrap;border-top:1px solid {LINE};border-bottom:1px solid {LINE};--padding-top:16px;--padding-bottom:16px;--padding-left:0;--padding-right:0;margin:40px 0 32px}}
.abc-share-label .elementor-heading-title{{font-size:14px;color:{MUTED};margin:0;font-weight:400;font-family:Roboto,Arial,sans-serif}}

/* Author box (same text as the previous theme author box) */
.e-con.abc-author{{border:1px solid {LINE};border-left:4px solid {GREEN};border-radius:10px;--padding-top:28px;--padding-bottom:28px;--padding-left:28px;--padding-right:28px;--gap:24px;--row-gap:24px;--column-gap:24px;--align-items:flex-start;background:#fff;box-shadow:0 6px 24px rgba(30,38,51,.06)}}
.abc-author-photo{{flex:none;width:104px}}
.abc-author-photo img{{width:104px;height:104px;border-radius:50%;object-fit:cover;box-shadow:0 4px 14px rgba(30,38,51,.18);border:3px solid #fff;display:block}}
.abc-author-text{{flex:1 1 0;min-width:0;font-size:15px;line-height:1.7;color:{TEXT}}}
.abc-author-text p{{margin:0 0 14px}}
.abc-author-text .abc-kicker{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:{GREEN};margin:0 0 4px}}
.abc-author-text .abc-author-name{{font-size:24px;line-height:1.25;margin:0 0 6px;font-weight:700;font-family:Roboto,Arial,sans-serif}}
.abc-author-text .abc-author-name a{{color:{HEADING};text-decoration:none}}
.abc-author-text .abc-author-name a:hover{{color:{NAVY}}}
.abc-author-text .abc-credline{{font-size:13px;line-height:1.5;color:{GREEN};margin:0 0 16px}}
.abc-credentials{{background:{SOFT};border-radius:8px;padding:16px 20px;margin:4px 0 18px}}
.abc-credentials strong{{display:block;color:{HEADING};font-size:15px;margin-bottom:8px}}
.abc-credentials ul{{list-style:none;margin:0;padding:0}}
.abc-credentials li{{position:relative;padding-left:24px;margin:0 0 8px;font-size:14px;line-height:1.5}}
.abc-credentials li:last-child{{margin-bottom:0}}
.abc-credentials li::before{{content:"";position:absolute;left:2px;top:.45em;width:10px;height:10px;border-radius:50%;border:2.5px solid {NAVY}}}
.abc-author-links{{display:flex;flex-wrap:wrap;gap:10px;margin:0!important}}
.abc-author-links a{{display:inline-block;font-size:14px;font-weight:500;text-decoration:none;border-radius:4px;padding:9px 16px;border:1.5px solid {NAVY};color:{NAVY}}}
.abc-author-links a:hover{{background:{NAVY};color:#fff}}
.abc-author-links a+a{{background:{GREEN};border-color:{GREEN};color:#fff}}
.abc-author-links a+a:hover{{background:{GREEN_DARK};border-color:{GREEN_DARK}}}

/* Related articles */
.e-con.abc-related{{--padding-top:48px;--padding-bottom:0;--padding-left:0;--padding-right:0;--gap:16px;--row-gap:16px;--column-gap:16px}}
.abc-related-title .elementor-heading-title{{font-size:28px;color:{HEADING};font-weight:700;margin:0;font-family:Roboto,Arial,sans-serif}}
.abc-related-posts .elementor-post{{border:1px solid {LINE};border-radius:6px;overflow:hidden;background:#fff;transition:box-shadow .2s,transform .2s}}
.abc-related-posts .elementor-post:hover{{box-shadow:0 8px 24px rgba(30,38,51,.1);transform:translateY(-2px)}}
.abc-related-posts .elementor-post__thumbnail__link{{margin-bottom:0!important}}
.abc-related-posts .elementor-post__text{{padding:14px 16px 18px}}
.abc-related-posts .elementor-post__title,.abc-related-posts .elementor-post__title a{{font-size:16px;line-height:1.35;color:{HEADING};font-weight:700}}

/* Mobile call / quote bar */
.e-con.abc-helpers{{--padding-top:0;--padding-bottom:0;--padding-left:0;--padding-right:0;--min-height:0}}
.abc-mobile-bar{{display:none}}

/* Tablet and below: stack layout, inline TOC */
@media (max-width:1024px){{
  .abc-hero-img{{width:100%}}
  .e-con.abc-hero-text{{--width:100%}}
  .abc-hero-img img{{aspect-ratio:16/9;max-height:none}}
  .e-con.abc-hero{{--gap:24px;--row-gap:24px;--column-gap:24px;--padding-top:32px;--padding-bottom:36px}}
  .e-con.abc-article{{max-width:none;width:100%}}
  .e-con.abc-sidebar{{--width:100%}}
  .e-con.abc-sticky{{position:static}}
  .e-con.abc-body{{--gap:36px;--row-gap:36px;--column-gap:36px;--padding-top:28px}}
}}
/* Phones */
@media (max-width:767px){{
  .e-con.abc-hero,.e-con.abc-body{{--padding-left:16px;--padding-right:16px}}
  .e-con.abc-hero{{--padding-top:24px;--padding-bottom:28px}}
  .e-con.abc-author{{--padding-left:20px;--padding-right:20px}}
  /* tables become one card per row */
  .abc-content figure.wp-block-table{{box-shadow:none;background:transparent;overflow-x:auto}}
  .abc-content figure.wp-block-table:has(table.abc-stack){{overflow:visible}}
  .abc-content .wp-block-table table.abc-stack{{min-width:0}}
  .abc-content table.abc-stack,.abc-content table.abc-stack tbody{{display:block}}
  .abc-content table.abc-stack tr.abc-thead{{display:none}}
  .abc-content table.abc-stack tr{{display:block;border-radius:10px;overflow:hidden;margin:0 0 12px;box-shadow:0 4px 16px rgba(30,38,51,.08);border:1px solid {LINE}}}
  .abc-content .wp-block-table table.abc-stack td{{display:grid;grid-template-columns:40% 1fr;gap:10px;padding:10px 14px;background:#fff!important;border-bottom:1px solid {LINE}}}
  .abc-content .wp-block-table table.abc-stack td::before{{content:attr(data-label);font-size:12px;font-weight:600;color:{MUTED};text-transform:uppercase;letter-spacing:.04em}}
  .abc-content .wp-block-table table.abc-stack td:first-child{{display:block;background:{NAVY}!important;color:#fff!important}}
  .abc-content .wp-block-table table.abc-stack td:first-child::before{{display:none}}
  .abc-content .wp-block-table table.abc-stack td:last-child{{border-bottom:0}}
  .abc-title .elementor-heading-title{{font-size:30px}}
  .abc-dek,.abc-dek p{{font-size:16px}}
  .abc-content{{font-size:16px}}
  .abc-content h2{{font-size:23px}}
  .abc-mobile-bar{{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:9998;box-shadow:0 -4px 16px rgba(0,0,0,.12)}}
  .abc-mobile-bar a{{padding:15px 10px;text-align:center;font-weight:700;text-decoration:none;color:#fff;font-size:15px;font-family:Roboto,Arial,sans-serif}}
  .abc-mobile-bar a:first-child{{background:{NAVY}}}
  .abc-mobile-bar a:last-child{{background:{GREEN}}}
  body.single-post{{padding-bottom:52px}}
}}
"""

page_settings = {
    "preview_type": "single/post",
    "preview_id": PREVIEW_POST_ID,
    "custom_css": CSS.strip(),
}

out = {"title": "Single Post – New Layout", "type": "single-post",
       "content": content, "page_settings": page_settings}
with open(os.path.join(HERE, "single-post-template.json"), "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("elements:", sum(1 for _ in json.dumps(content).split('"elType"')) - 1, "css bytes:", len(CSS))
