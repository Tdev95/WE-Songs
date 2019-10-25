// Show the histogram
function showHistogram (endpoint, query, field) {
	fetch ('/'+endpoint+query)
		.then (
			function (response) {
				if (response.status == 200) {
					response.json().then(function (data) {
						var txt = '<img src="';
						txt += createLink (data, endpoint, query, field);
						txt += '">'
						document.getElementById("resultHistogram").innerHTML = txt;
					});
				} else {
					alert ("Error: " + response.status);
				}
			}
		);
}

// Create the link for QuickChart
function createLink (data, endpoint, query, field) {
	var width = computeWidth (Object.keys(data).length);
	var txt = 'https://quickchart.io/chart?width='+width+'&bkg=white&c=';
	txt += chartData (data, endpoint, query, field);
	return txt;
}

// Create the data for QuickChart image in JSON format
function chartData (data, endpoint, query, field) {
	var txt = 
		"{" +
			"type: 'bar'," +
			"data: {" +
				"labels: [";
	// Add labels (the keys)
	prefix = "";
	for (y in data) {
		txt += prefix + "'"+ (data[y][field]+"").replace("&","n").replace("'","`") + "'";
		prefix = ",";
	}
	txt +=		"]," +
				"datasets: [{" +
					"label: '"+endpoint+"'," +
					"data: [";
	// Add data (the count)
	prefix = "";
	for (y in data) {
		txt += prefix + data[y].count;
		prefix = ",";
	}
	txt +=			"]" +
				"}]" +
			"}," +
			"options: {" +
				"title: {" +
					"display: true," +
					"text: '" + '/'+endpoint+query.replace("&"," ") + "'," +
				"}," +
				"legend: {" +
					"display: false," +
				"}" +
			"}" +
		"}";
	return txt;
}

// Compute the width of the image (depending on the number of elements (=size))
function computeWidth (size) {
	var min = 12, max = 460;
	var minWidth = 500, maxWidth = 4000;
	if (size <= min)
		return minWidth;
	if (size >= max)
		return maxWidth;
	return minWidth + (maxWidth - minWidth) * ((size - min)/(max - min));
}