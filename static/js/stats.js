// Show the table
function showStats (artistId, year) {
	var query = createQuery (artistId, year);
	fetch ('/stats'+query)
		.then (
			function (response) {
				if (response.status = 200) { // show the result
					response.json().then(function (data) {
						var txt = '';
						txt += 'median: ' + data['median'] + '<br>';
						txt += 'mean: ' + data['mean'] + '<br>';
						txt += 'standard deviation: ' + data['standard deviation'];
						document.getElementById("resultStats").innerHTML = txt;
					});
				} else {
					alert ("Error: " + response.status);
				}
			}
		);
}

function createQuery (artisId, year) {
	var query = '';
	if (artisId)
		query += 'artist_id='+artisId;
	if (year) {
		if (query)
			query += '&';
		query += 'year='+year;
	}
	if (query)
		query = '?' + query;
	return query;
}