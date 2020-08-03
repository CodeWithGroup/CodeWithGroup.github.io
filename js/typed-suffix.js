var intervalTypingMilliseconds = 300;
var intervalChangeText = 5000;
var lastSuffixIndex = 10;

var suffixes = [
    "BEN",
    "DREW",
    "EDWARD",
    "GARETH",
    "HARRY",
    "JIM",
    "LIAM",
    "LIZ",
    "KEIRAN",
    "SIMON",
    "US"
];

function showText(target, message, index, maxInterval) {
    if (index < message.length) {
        $(target).append(message[index++]);
        var randomTypingInterval = Math.floor(Math.random() * maxInterval);
        setTimeout(function() {
            showText(target, message, index, maxInterval);
        }, randomTypingInterval);
    }
}

function showSuffix(target, suffixInterval) {
    var suffixIndex = Math.floor(Math.random() * suffixes.length);
    while (suffixIndex === lastSuffixIndex) {
        var suffixIndex = Math.floor(Math.random() * suffixes.length);
    }
    
    setTimeout(function() {
        $(target).text('');
        showText(target, suffixes[suffixIndex], 0, intervalTypingMilliseconds);
        showSuffix(target, suffixInterval)
    }, intervalChangeText);
}

$(function() {
    showSuffix("#suffix", intervalChangeText);
})