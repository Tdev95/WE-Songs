function keysHistogram (genre, hotnessThreshold) {
	showHistogram (
		'keys',
		createQuery (genre, hotnessThreshold),
		'key'
	);
}

function createQuery (genre, hotnessThreshold) {
	query = '';
	if (genre)
		query += 'genre='+genre;
	if (hotnessThreshold) {
		if (query)
			query += '&';
		query += 'hotnessThreshold='+hotnessThreshold;
	}
	if (query)
		query = '?' + query;
	return query;
}