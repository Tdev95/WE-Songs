// Function to add a song with id=songId to the database
function addSong (songId) {
	var formData = toJSONString ();
	fetch ('/songs/'+songId, {method: 'POST', body: formData})
		.then (
			function (response) {
				if (response.status == 201)
					alert("Added song with id " + songId);
				else if (response.status == 400)
					alert ("Bad request");
				else if (response.status == 409)
					alert ("Song with id " + songId + " already in dataset");
				else
					alert("Error: " + response.status);
			}
		);
}

// Function to update a song with id=songId in the database
// Note that all fields are updated (with new or old value)
function modifySong (songId) {
	var formData = toJSONString ();
	fetch ('/songs/'+songId, {method: 'PATCH', body: formData})
		.then (
			function (response) {
				if (response.status == 200)
					alert("Modified song with id " + songId);
				else if (response.status == 400)
					alert ("Bad request");
				else if (response.status == 404)
					alert ("Did not find song with id " + songId);
				else
					alert("Error: " + response.status);
			}
		);
}

// Turn the form into a JSON string
function toJSONString() {
	var obj = {};
	var form = document.forms['form'];
	var elements = form.querySelectorAll( "input, select, textarea" );
	for( var i = 0; i < elements.length; ++i ) {
		var element = elements[i];
		var name = element.name;
		if (name == 'songId')
			name = 'id';
		var value = element.value;
		if( name ) {
			obj[ name ] = value;
		}
	}
	return JSON.stringify(obj);
}

// Delete a song with id=songId from the database
function deleteSong (songId) {
	fetch ('/songs/'+songId, {method: 'DELETE'})
		.then (
			function (response) {
				if (response.status == 201)
					alert("No content/Deleted song with id " + songId);
				else if (response.status == 400)
					alert ("Bad request");
				else if (response.status == 404)
					alert ("Did not find song with id " + songId);
				else
					alert("Error: " + response.status);
			}
		);
}

// Get a a song with id=songId from the database and show its values in the form
function searchSong (songId) {
	fetch ('/songs/'+songId)
		.then (
			function (response) {
				if (response.status == 200) {
					response.json().then(function (data) {
						oForm = document.forms['form'];
						oForm.elements["artist_id"].value = data.artist_id;
						oForm.elements["release_id"].value = data.release_id;
						oForm.elements["artist_mbtags"].value = data.artist_mbtags;
						oForm.elements["artist_mbtags_count"].value = data.artists_mbtags_count;
						oForm.elements["bars_confidence"].value = data.bars_confidence;
						oForm.elements["bars_start"].value = data.bars_start;
						oForm.elements["beats_confidence"].value = data.beats_confidence;
						oForm.elements["beats_start"].value = data.beats_start;
						oForm.elements["duration"].value = data.duration;
						oForm.elements["end_of_fade_in"].value = data.end_of_fade_in;
						oForm.elements["hotness"].value = data.hotness;
						oForm.elements["key_in"].value = data.key_in;
						oForm.elements["key_confidence"].value = data.key_confidence;
						oForm.elements["loudness"].value = data.loudness;
						oForm.elements["mode"].value = data.mode;
						oForm.elements["mode_confidence"].value = data.mode_confidence;
						oForm.elements["start_of_fade_out"].value = data.start_of_fade_out;
						oForm.elements["tatums_confidence"].value = data.tatums_confidence;
						oForm.elements["tatums_start"].value = data.tatums_start;
						oForm.elements["tempo"].value = data.tempo;
						oForm.elements["time_signature"].value = data.time_signature;
						oForm.elements["time_signature_confidence"].value = data.time_signature_confidence;
						oForm.elements["title"].value = data.title;
						oForm.elements["year"].value = data.year;
					});
				} else if (response.status == 400) {
					alert("Bad request");
				} else if (response.status == 404) {
					alert ("Did not find song with id " + songId);
				} else {
					alert("Error: " + response.status);
				}
			}
		);
}