function artistsTable (name, genre, sort, page) {
	showTable (
		'artists',
		createQuery (name, genre, sort, page)
	);
}

function createQuery (name, genre, sort, page) {
	query = '';
	if (name)
		query += 'name='+name;
	if (genre) {
		if (query)
			query += '&';
		query += 'genre='+genre;
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
	txt += "<th>ID</th>"
	txt += "<th>songs</th>"
	txt += "<th>familiarity</th>"
	txt += "<th>hotness</th>"
	txt += "<th>lattitude</th>"
	txt += "<th>location</th>"
	txt += "<th>longitude</th>"
	txt += "<th>name</th>"
	txt += "<th>similar</th>"
	txt += "<th>terms</th>"
	txt += "<th>terms_freq</th>"
	txt += "</tr>"
	for (x in data) {
		txt += "<tr>";
		txt += "<td>" + data[x].id + "</td>";
		txt += "<td> <a href='" + data[x].songs + "'>songs</a>" + "</td>";
		txt += "<td>" + data[x].familiarity + "</td>";
		txt += "<td>" + data[x].hotness + "</td>";
		txt += "<td>" + data[x].lattitude + "</td>";
		txt += "<td>" + data[x].location + "</td>";
		txt += "<td>" + data[x].longitude + "</td>";
		txt += "<td>" + data[x].name + "</td>";
		txt += "<td>" + data[x].similar + "</td>";
		txt += "<td>" + data[x].terms + "</td>";
		txt += "<td>" + data[x].terms_freq + "</td>";
		txt += "</tr>";
	}
	txt += "</table>"
	return txt;
}