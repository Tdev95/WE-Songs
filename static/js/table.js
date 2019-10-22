function showTable (endpoint, query) {
	fetch ('/'+endpoint+query)
		.then (
			function (response) {
				if (response.status != 200) {
					alert('Error: ' + response.status);
				} else { // show the result
					response.json().then(function (data) {
						table = createTable (data);
						document.getElementById("resultTable").innerHTML = table;
					});
				}
			}
		);
}