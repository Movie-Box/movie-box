let deferredInstallPrompt = null;
const installButton = document.getElementById('butInstall');
const otherInstallButton = document.getElementById('installButton');
if (installButton !== null) {
    installButton.addEventListener('click', installPWA);
}
if (otherInstallButton !== null) {
    otherInstallButton.addEventListener('click', installPWA);
}

window.addEventListener('beforeinstallprompt', saveBeforeInstallPromptEvent);

function saveBeforeInstallPromptEvent(evt) {
    deferredInstallPrompt = evt;
    if (installButton !== null) {
        installButton.removeAttribute('hidden');
    }
    if (otherInstallButton !== null) {
        otherInstallButton.removeAttribute('hidden');
    }
}

function installPWA(evt) {
    deferredInstallPrompt.prompt();
    if (installButton !== null) {
        installButton.setAttribute('hidden', true);
    }
    if (otherInstallButton !== null) {
        otherInstallButton.setAttribute('hidden', true);
    }
    deferredInstallPrompt.userChoice
        .then((choice) => {
            if (choice.outcome === 'accepted') {
                console.log('User accepted the add to homescreen prompt', choice);
            } else {
                console.log('User dismissed the add to homescreen prompt', choice);
            }
            deferredInstallPrompt = null;
        });
}

window.addEventListener('appinstalled', logAppInstalled);

function logAppInstalled(evt) {
    console.log('App was installed.', evt);
}