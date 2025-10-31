let map;
let marker;
let geocoder;

function handleAddressSelected(address, location = null) {
    document.getElementById("id_delivery_address").value = address;
    document.getElementById("address-input").value = address;
    if (!marker) {
        marker = new google.maps.Marker({
            map: map,
            draggable: true,
            animation: google.maps.Animation.DROP,
        });
    }
    if (location) {
        marker.setPosition(location);
        map.setCenter(location);
    }
}

function geocodeLatLng(latlng) {
    geocoder.geocode({ location: latlng }, (results, status) => {
        if (status === "OK" && results[0]) {
            handleAddressSelected(results[0].formatted_address, latlng);
        } else {
            console.log("Адресу не знайдено або помилка: " + status);
        }
    });
}

function initMap() {
    const position = { lat: 49.550844, lng: 27.938196 };
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: position,
    });

    geocoder = new google.maps.Geocoder();

    const input = document.getElementById("address-input");
    const autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo("bounds", map);

    autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();
        if (!place.geometry || !place.geometry.location) return;
        handleAddressSelected(place.formatted_address, place.geometry.location);
    });

    map.addListener("click", (event) => {
        geocodeLatLng(event.latLng);
    });
}
