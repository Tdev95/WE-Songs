function showHistogram (endpoint, query, field) {
	fetch ('/'+endpoint+query)
		.then (
			function (response) {
				if (response.status != 200) {
					alert('Error: ' + response.status);
				} else {
					response.json().then(function (data) {
						var width = computeWidth (Object.keys(data).length);
						txt = '<img src="https://quickchart.io/chart?width='+width+'&bkg=white&c=';
						txt += 
							"{" +
								"type: 'bar'," +
								"data: {" +
									"labels: [";
						// Add labels (the keys)
						prefix = "";
						for (y in data) {
							txt += prefix + "'"+ data[y][field] + "'";
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
								"}" +
							"}";
						txt += '">'
						document.getElementById("resultHistogram").innerHTML = txt;
					});
				}
			}
		);
}

function computeWidth (size) {
	var min = 12, max = 460;
	var minWidth = 500, maxWidth = 4000;
	if (size <= min)
		return minWidth;
	if (size >= max)
		return maxWidth;
	return minWidth + (maxWidth - minWidth) * ((size - min)/(max - min));
}