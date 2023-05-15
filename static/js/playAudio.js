window.onload = function() {
    const play = document.getElementById('overlay-icon-play');
    const pause = document.getElementById('overlay-icon-pause');
    const audio = document.getElementById('crying-out-preview');

    const handlePauseClick = () => {
        audio.pause();
        pause.style.visibility = 'hidden';
        pause.style.opacity = 0;
        play.style.visibility = 'visible';
        play.style.opacity = 1;
    }

    const handlePlayClick = () => {
        audio.play();
        play.style.visibility = 'hidden';
        play.style.opacity = 0
        pause.style.visibility = 'visible';
        pause.style.opacity = 1;
    };

    play.addEventListener('click', handlePlayClick, false);
    pause.addEventListener('click', handlePauseClick, false);
    audio.addEventListener('ended', handlePauseClick, false);
};