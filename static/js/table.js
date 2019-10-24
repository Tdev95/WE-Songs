// Show the table
function showTable (endpoint, query) {
	fetch ('/'+endpoint+query)
		.then (
			function (response) {
				if (response.status != 200) {
					alert('Error: ' + response.status);
				} else { // show the result
					response.json().then(function (data) {
						table = createTable (data); // artists and songs make their own table
						document.getElementById("resultTable").innerHTML = table;
					});
				}
			}
		);
}