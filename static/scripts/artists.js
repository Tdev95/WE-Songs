function showTable (name, genre, sort, page) {
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
	alert('query'+query);
	fetch ('/artists'+query)
		.then (
			function (response) {
				if (response.status != 200) {
					alert('Error: ' + response.status);
				} else { // show the result
					alert('Succes');
					response.json().then(function (data) {
						txt = "<table border='1'>";
						for (x in data) {
							txt += "<tr>";
							txt += "<td>" + data[x].name + "</td>";
							txt += "<td>" + data[x].terms + "</td>";
							txt += "<td>" + data[x].hotness + "</td>";
							txt += "<tr>";
						}
						txt += "</table>"
						document.getElementById("resultTable").innerHTML = txt;
					});
				}
			}
		);
}