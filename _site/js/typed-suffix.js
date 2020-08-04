var intervalTypingMillisecondsBase = 50;
var intervalTypingMaxMilliseconds = 200;
var intervalChangeText = 4000;

var currentSuffixIndex, lastSuffixIndex, lastSuffixButOneIndex;

var languages = [
    "C#",
    "CSS",
    "HTML",
    "JAVA",
    "JS",
    "PYTHON",
    "SQL"
]

var people = [
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
        
        var typingInterval = maxInterval - intervalTypingMillisecondsBase;
        if (typingInterval < 0) {
            typingInterval = 0;
        }

        typingInterval = intervalTypingMillisecondsBase + Math.floor(Math.random() * typingInterval);
        setTimeout(function() {
            showText(target, message, index, maxInterval);
        }, typingInterval);
    }
}

function showSuffix(target, suffixOptions, suffixInterval) {
    while (currentSuffixIndex === lastSuffixIndex || currentSuffixIndex === lastSuffixButOneIndex) {
        currentSuffixIndex = Math.floor(Math.random() * suffixOptions.length);
    }
    lastSuffixButOneIndex = lastSuffixIndex;    
    lastSuffixIndex = currentSuffixIndex;
    
    setTimeout(function() {
        $(target).text('');
        showText(target, suffixOptions[currentSuffixIndex], 0, intervalTypingMaxMilliseconds);
        showSuffix(target, suffixOptions, suffixInterval)
    }, intervalChangeText);
}

$(function() {
    var suffixOptions = languages;
    currentSuffixIndex = lastSuffixIndex = lastSuffixButOneIndex = suffixOptions.length - 1;
    showSuffix("#suffix", suffixOptions, intervalChangeText);
})