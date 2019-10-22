function genresHistogram (year, threshold) {
	showHistogram (
		'genres',
		createQuery (year, threshold),
		'genre'
	);
}

function createQuery (year, threshold) {
	query = '';
	if (year)
		query += 'year='+year;
	if (threshold) {
		if (query)
			query += '&';
		query += 'threshold='+threshold;
	}
	if (query)
		query = '?' + query;
	return query;
}