function songsTable (genre, release, artist, year, sort, page) {
	showTable (
		'songs',
		createQuery (genre, release, artist, year, sort, page)
	);
}

function createQuery (genre, release, artist, year, sort, page) {
	query = '';
	if (genre)
		query += 'genre='+genre;
	if (release) {
		if (query)
			query += '&';
		query += 'release='+release;
	}
	if (artist) {
		if (query)
			query += '&';
		query += 'artist='+artist;
	}
	if (year) {
		if (query)
			query += '&';
		query += 'year='+year;
	}
	if (sort) {
		if (query)
			query += '&';
		query += 'sort='+sort;
	}
	if (page) {
		if (query)
			query += '&';
		query += 'page='+page;
	}
	if (query)
		query = '?' + query;
	return query;
}

function createTable (data) {
	var txt = "<table border='1'>";
	txt += "<tr>";
	txt += "<th>id</th>"
	txt += "<th>artist</th>"
	txt += "<th>release</th>"
	txt += "<th>artist_mbtags</th>"
	txt += "<th>artists_mbtags_count</th>"
	txt += "<th>bars_confidence</th>"
	txt += "<th>bars_start</th>"
	txt += "<th>beats_confidence</th>"
	txt += "<th>beats_start</th>"
	txt += "<th>duration</th>"
	txt += "<th>end_of_fade_in</th>"
	txt += "<th>hotness</th>"
	txt += "<th>key_in</th>"
	txt += "<th>key_confidence</th>"
	txt += "<th>loudness</th>"
	txt += "<th>mode</th>"
	txt += "<th>mode_confidence</th>"
	txt += "<th>start_of_fade_out</th>"
	txt += "<th>tatums_confidence</th>"
	txt += "<th>tatums_start</th>"
	txt += "<th>tempo</th>"
	txt += "<th>time_signature</th>"
	txt += "<th>time_signature_confidence</th>"
	txt += "<th>title</th>"
	txt += "<th>year</th>"
	txt += "</tr>"
	for (x in data) {
		txt += "<tr>";
		txt += "<td>" + data[x].id + "</td>";
		txt += "<td> <a href='" + data[x].artist + "'>artist</a>" + "</td>";
		txt += "<td> <a href='" + data[x].release + "'>release</a>" + "</td>";
		txt += "<td>" + data[x].artist_mbtags + "</td>";
		txt += "<td>" + data[x].artists_mbtags_count + "</td>";
		txt += "<td>" + data[x].bars_confidence + "</td>";
		txt += "<td>" + data[x].bars_start + "</td>";
		txt += "<td>" + data[x].beats_confidence + "</td>";
		txt += "<td>" + data[x].beats_start + "</td>";
		txt += "<td>" + data[x].duration + "</td>";
		txt += "<td>" + data[x].end_of_fade_in + "</td>";
		txt += "<td>" + data[x].hotness + "</td>";
		txt += "<td>" + data[x].key_in + "</td>";
		txt += "<td>" + data[x].key_confidence + "</td>";
		txt += "<td>" + data[x].loudness + "</td>";
		txt += "<td>" + data[x].mode + "</td>";
		txt += "<td>" + data[x].mode_confidence + "</td>";
		txt += "<td>" + data[x].start_of_fade_out + "</td>";
		txt += "<td>" + data[x].tatums_confidence + "</td>";
		txt += "<td>" + data[x].tatums_start + "</td>";
		txt += "<td>" + data[x].tempo + "</td>";
		txt += "<td>" + data[x].time_signature + "</td>";
		txt += "<td>" + data[x].time_signature_confidence + "</td>";
		txt += "<td>" + data[x].title + "</td>";
		txt += "<td>" + data[x].year + "</td>";
		txt += "</tr>";
	}
	txt += "</table>"
	return txt;
}