/* City-centre coordinates are bundled locally; no geolocation or online lookup. */
(() => {
  'use strict';
  const cities = {
    Nairobi: { name: 'Nairobi', latitude: -1.28333, longitude: 36.81667 },
    Accra: { name: 'Accra', latitude: 5.55602, longitude: -0.19690 },
    Kigali: { name: 'Kigali', latitude: -1.94995, longitude: 30.05885 },
    CapeTown: { name: 'Cape Town', latitude: -33.92584, longitude: 18.42322 },
    AddisAbaba: { name: 'Addis Ababa', latitude: 9.02491860421, longitude: 38.7356223148 },
  };
  const phraseCities = {
    'hapa kazi tu': 'Nairobi',
    "as'hamb', there's a seat": 'CapeTown',
    'all hands on deck': 'AddisAbaba',
    'tukutane production': 'Nairobi',
    'tupo site, kata simu': 'Nairobi',
    'akwaaba, builders': 'Accra',
    'chale, ship am': 'Accra',
    'tugende, ship it': 'Kigali',
  };
  function angle(value, positive, negative) {
    const minutes = Math.round(Math.abs(value) * 60);
    return `${Math.floor(minutes / 60)}°${minutes % 60}′${value < 0 ? negative : positive}`;
  }
  function format(city) {
    return `${angle(city.latitude, 'N', 'S')} ${angle(city.longitude, 'E', 'W')}`;
  }
  window.LabsLocations = Object.freeze({
    cities, phraseCities, format,
    forPhrase(phrase) { return cities[phraseCities[phrase] || 'Nairobi']; },
  });
  window.LabsActiveCity = cities.Nairobi;
})();
