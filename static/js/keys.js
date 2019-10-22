function keysHistogram (genre, threshold) {
	width = '';
	showHistogram (
		'keys',
		createQuery (genre, threshold),
		'key'
	);
}

function createQuery (genre, threshold) {
	query = '';
	if (genre)
		query += 'genre='+genre;
	if (threshold) {
		if (query)
			query += '&';
		query += 'threshold='+threshold;
	}
	if (query)
		query = '?' + query;
	return query;
}