<?php
/**
 * Single post title: always break the line after a colon.
 *
 * "Custom Closets in Fort Lauderdale: Cost, Timeline, and How to Choose a Builder"
 * renders as
 *   <span class="title-main">Custom Closets in Fort Lauderdale:</span>
 *   <span class="title-sub">Cost, Timeline, and How to Choose a&nbsp;Builder</span>
 *
 * Both spans are display:block (see CSS below), so a word can never be left
 * alone on the same line after the colon. The last two words are joined with a
 * non-breaking space so the title never ends with a single word on its own line.
 * Titles without a colon only get the non-breaking space.
 *
 * Add to the child theme's functions.php (or a code snippets plugin).
 */

if ( ! function_exists( 'abc_format_post_title' ) ) {
	function abc_format_post_title( $title ) {
		$title = trim( (string) $title );

		// Join the last two words so the final line is never a single word.
		$keep_last_two = static function ( $text ) {
			return preg_replace( '/\s+(\S+)$/u', '&nbsp;$1', $text );
		};

		// Split only on a colon followed by a space, so times like "10:30" are left alone.
		if ( preg_match( '/^(.+?:)\s+(.+)$/u', $title, $m ) ) {
			return '<span class="title-main">' . esc_html( $m[1] ) . '</span> '
				. '<span class="title-sub">' . $keep_last_two( esc_html( $m[2] ) ) . '</span>';
		}

		return $keep_last_two( esc_html( $title ) );
	}
}

/**
 * Option A, custom theme template (single.php):
 *   <h1 class="entry-title"><?php echo abc_format_post_title( get_the_title() ); ?></h1>
 *
 * Option B, Elementor Theme Builder: use a Shortcode widget with an H1 wrapper,
 * or an HTML widget, containing [abc_post_title].
 */
add_shortcode( 'abc_post_title', static function () {
	return '<h1 class="entry-title">' . abc_format_post_title( get_the_title() ) . '</h1>';
} );

/*
CSS to add with the template styles:

.single-post h1 .title-main,
.single-post h1 .title-sub { display: block; text-wrap: balance; }
*/
