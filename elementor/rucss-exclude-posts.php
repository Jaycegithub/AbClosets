
/**
 * AB Closets: turn off WP Rocket "Remove Unused CSS" on blog posts only.
 *
 * The Elementor single post template needs its full CSS. WP Rocket already supports
 * excluding a single post from Remove Unused CSS (the "Remove Unused CSS" box in the
 * post editor's WP Rocket panel, stored as _rocket_exclude_remove_unused_css).
 * This reports that box as ticked for every post of type "post", including new ones.
 * Pages, the homepage and service pages are not affected.
 */
add_filter( 'get_post_metadata', static function ( $value, $object_id, $meta_key ) {
	if ( '_rocket_exclude_remove_unused_css' === $meta_key && 'post' === get_post_type( $object_id ) ) {
		return [ 1 ];
	}
	return $value;
}, 10, 3 );
