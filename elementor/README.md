# Single Post template (Elementor Theme Builder)

Standard Elementor/PRO Elements widgets only (no Atomic Editor). Built and updated through the WordPress REST API.

- Template on the site: `elementor_library` post **3167**, type `single-post`, "Single Post – New Layout"
- Source: `build_single_post_template.py` generates `single-post-template.json` (element tree + document Custom CSS)
- Title colon rule: `../mockups/title-colon-break.php` (install in the theme's functions.php or a snippets plugin)

## Update the template
1. Edit and run `python3 build_single_post_template.py`
2. `POST /wp-json/wp/v2/elementor_library/3167` with `meta._elementor_data` (JSON string) and `meta._elementor_page_settings`
3. `DELETE /wp-json/elementor/v1/cache` to regenerate Elementor CSS

## Display conditions
`POST /wp-json/elementor/v1/site-editor/templates-conditions/3167`
- Test (current): `{"conditions":[{"type":"include","name":"singular","sub_name":"post","sub_id":"2534"}]}`
- All posts: `{"conditions":[{"type":"include","name":"singular","sub_name":"post"}]}`
- Undo: `{"conditions":[]}`
