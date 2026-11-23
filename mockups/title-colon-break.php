<?php
/**
 * AB Closets: single post title, always break the line after a colon.
 *
 * Works with Elementor's standard "Post Title" widget in the Single Post template.
 * "Custom Closets in Fort Lauderdale: Cost, Timeline, and How to Choose a Builder"
 * is output as
 *   <h1 ...><span class="title-main">Custom Closets in Fort Lauderdale:</span>
 *           <span class="title-sub">Cost, Timeline, and How to Choose a&nbsp;Builder</span></h1>
 * The template CSS makes both spans display:block, so no single word is left on the
 * colon line. The last two words are joined with a non-breaking space so a title never
 * ends with one word on its own line. Titles without ": " only get the non-breaking space.
 *
 * Install: add to the theme's functions.php, or as a PHP snippet in a code snippets plugin.
 * If this is not installed the template still works; titles just wrap normally.
 */

if ( ! function_exists( 'abc_split_title_html' ) ) {
	/**
	 * @param string $html Title text as already escaped by WordPress/Elementor.
	 */
	function abc_split_title_html( $html ) {
		$html = trim( $html );

		$keep_last_two = static function ( $text ) {
			return preg_replace( '/\s+([^\s<>]+)$/u', '&nbsp;$1', $text );
		};

		// Split only on a colon followed by a space, so times like "10:30" are left alone.
		if ( preg_match( '/^(.+?:)\s+(.+)$/us', $html, $m ) ) {
			return '<span class="title-main">' . $m[1] . '</span> '
				. '<span class="title-sub">' . $keep_last_two( $m[2] ) . '</span>';
		}

		return $keep_last_two( $html );
	}
}

add_filter( 'elementor/widget/render_content', static function ( $content, $widget ) {
	if ( 'theme-post-title' !== $widget->get_name() || ! is_singular( 'post' ) ) {
		return $content;
	}

	// Only touch the plain-text title inside the heading tag (no nested links/markup).
	return preg_replace_callback(
		'#(<h1\b[^>]*>)([^<]+)(</h1>)#u',
		static function ( $m ) {
			return $m[1] . abc_split_title_html( $m[2] ) . $m[3];
		},
		$content,
		1
	);
}, 10, 2 );
