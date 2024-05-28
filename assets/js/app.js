let previousScene = 1;
let section;


$(document).ready(function() {
    // Initialiser la première scène
    initializeScene(1);




});



function changeScene(sectionNumber) {
    // Arrêter et nettoyer la scène précédente s'il y en a une
    if (previousScene) {
        stopScene(previousScene);
    }

    // Initialiser la nouvelle scène
    initializeScene(sectionNumber);

    // Mettre à jour la référence de la scène précédente
    previousScene = sectionNumber;
}



// Fonction pour arrêter toutes les animations et les timers associés à une scène spécifique
function stopScene(sceneNumber) {
    switch (sceneNumber) {
        case 1:
            stopScene1();
            break;
        case 2:
            stopScene2();
            break;
        case 3:
            stopScene3();
            break;
        case 4:
            stopScene4();
            break;
        // Ajoutez d'autres cas pour les sections supplémentaires
        default:
            console.error("Scene not supported");
            break;
    }
}

function stopScene1() {
    // Sélectionner le conteneur principal de la page 1
    let container = document.querySelector('.app_container_page1');

    // Vérifier si le conteneur existe avant de le supprimer
    if (container) {
        container.remove();
    }
}

function stopScene2(){
    // Sélectionner le conteneur principal de la page 2
    let containerPage2 = document.querySelector('.app_container_page');

    // Vérifier si le conteneur existe avant de le supprimer
    if (containerPage2) {
        containerPage2.remove();
    }

}

function stopScene3(){

    // Sélectionner le conteneur principal de la page 2
    let containerPage2 = document.querySelector('.app_container_page');

    // Vérifier si le conteneur existe avant de le supprimer
    if (containerPage2) {
        containerPage2.remove();
    }


    // Sortis des élements de la scène 

}






















function initializeScene(sectionNumber) {

    // Appeler la fonction spécifique à chaque section
    switch (sectionNumber) {
        case 1:
            initializeScene1();
            break;
        case 2:
            initializeScene2();
            break;
        case 3:
            initializeScene3();
            break;
        case 4:
            initializeScene4();
            break;        
        // Ajoute d'autres cas pour les sections supplémentaires
        default:
            console.error("Section not supported");
            break;
    }
}



function initializeScene1() {

      // Création de l'élément div contenant
      let container = document.createElement('div');
      container.className = 'app_container_page1';
  
      // Création du bouton
      let button = document.createElement('button');
      button.className = 'btn-page1';
  
      // Création du texte du bouton
      let buttonTitle = document.createElement('h1');
      buttonTitle.className = 'btn-text-page1';
      buttonTitle.textContent = 'Try It !';
  
      // Assemblage des éléments
      button.appendChild(buttonTitle);
      container.appendChild(button);

      gsap.from(button, {duration: 1, y: -100, opacity: 0, ease: 'back.out(1.7)'});
  
      // Ajout du container à l'élément body ou à un autre élément spécifique de la page
      document.body.appendChild(container);
          // Ajouter un écouteur d'événements pour le bouton
        $('.btn-page1').click(function() {

            // Changer de scène
            changeScene(2);
        });

 


}


function initializeScene2() {

    // Conteneur principal pour la page 2
    const containerPage2 = document.createElement('div');
    containerPage2.className = 'app_container_page';

    // Création du header de la page 2
    const page2Header = document.createElement('div');
    page2Header.className = 'page2_header';

    // Ajout du logo
    const logoImg = document.createElement('img');
    logoImg.src = 'assets/img/logo.png';
    logoImg.alt = 'Dell Logo';
    logoImg.className = 'page2_logo';
    page2Header.appendChild(logoImg);


    // Ajout du titre de l'application
    const appName = document.createElement('h1');
    appName.className = 'appName';
    appName.textContent = 'Text AI';

    
    gsap.from(appName, {duration: 1, x:-100,opacity: 0, ease: 'back.out(1.7)'});
    page2Header.appendChild(appName);

    // Création du conteneur pour les liens
    const linkHeader = document.createElement('div');
    linkHeader.className = 'linkHeader';

    // Boutons Home et About
    const linkHome = document.createElement('button');
    linkHome.className = 'linkHome';
    linkHome.innerHTML = '<p>Home</p>';
    linkHeader.appendChild(linkHome);

    const linkAbout = document.createElement('button');
    linkAbout.className = 'linkAbout';
    linkAbout.innerHTML = '<p>About</p>';
    linkHeader.appendChild(linkAbout);

    page2Header.appendChild(linkHeader);
    containerPage2.appendChild(page2Header);

    // Création du contenu de la page 2
    const page2Content = document.createElement('div');
    page2Content.className = 'page2_content';

    // Contenu gauche
    const page2ContentLeft = document.createElement('div');
    page2ContentLeft.className = 'page2_content_left active';

    const menuHistoryClose = document.createElement('img');
    menuHistoryClose.src = 'assets/img/menu-close.png';
    menuHistoryClose.alt = 'menu-close';
    menuHistoryClose.className = 'menuHistoryClose';
    page2ContentLeft.appendChild(menuHistoryClose);

    const contentTitle = document.createElement('h1');
    contentTitle.className = 'page2_content_title';
    contentTitle.textContent = 'History';
    page2ContentLeft.appendChild(contentTitle);

    const line = document.createElement('div');
    line.className = 'line';
    page2ContentLeft.appendChild(line);

    const historyContent = document.createElement('div');
    historyContent.className = 'page2_content_history';
    page2ContentLeft.appendChild(historyContent);

    page2Content.appendChild(page2ContentLeft);

    // Contenu droit
    const page2ContentRight = document.createElement('div');
    page2ContentRight.className = 'page2_content_right';

    const menuHistoryOpen = document.createElement('img');
    menuHistoryOpen.src = 'assets/img/menu.png';
    menuHistoryOpen.alt = 'menu-open';
    menuHistoryOpen.className = 'menuHistoryOpen';
    page2ContentRight.appendChild(menuHistoryOpen);

    page2Content.appendChild(page2ContentRight);
    containerPage2.appendChild(page2Content);

    // Bas de page
    const page2Bottom = document.createElement('div');
    page2Bottom.className = 'page2_bottom';

    const chatText = document.createElement('div');
    chatText.className = 'chatText';

    const chatInput = document.createElement('input');
    chatInput.type = 'text';
    chatInput.className = 'chatInput';
    chatInput.placeholder = 'Type a message...';
    chatText.appendChild(chatInput);

    const chatSend = document.createElement('button');
    chatSend.className = 'chatSend';
    chatSend.textContent = 'Send';
    chatText.appendChild(chatSend);

    page2Bottom.appendChild(chatText);
    containerPage2.appendChild(page2Bottom);

    // Ajout du conteneur principal à la page
    document.body.appendChild(containerPage2);

    gsap.to(logoImg, {
        duration: 1, // Durée de l'animation en secondes
        x: 20, // Distance de déplacement à droite
        ease: 'power1.inOut', // Courbe d'animation
        repeat: 20, // Répéter indéfiniment
        yoyo: true // Inverser l'animation à chaque répétition
    });
    




    $('.page2_logo').click(function() {
        // Changer de scène
        changeScene(1);
    });
    $('.linkHome').click(function() {
        // Changer de scène
        changeScene(2);
    });
    $('.linkAbout').click(function() {
        // Changer de scène
        changeScene(3);
    });




    $('.menuHistoryClose').click(function() {
        $('.page2_content_left').toggleClass('active');
        $(".menuHistoryOpen").toggleClass('active');

    });
    $('.menuHistoryOpen').click(function() {
        $('.page2_content_left').toggleClass('active');
        $(".menuHistoryOpen").toggleClass('active');

    });

    // Element de la scène 

}
function initializeScene3(){
    // Element de la scène 
    function createAboutContent(parentElement, title, subTitle1, text1, subTitle2, text2) {
        const titleElement = document.createElement('h1');
        titleElement.className = 'page2_content_title_about';
        titleElement.textContent = title;
        parentElement.appendChild(titleElement);

        const line = document.createElement('div');
        line.className = 'line';
        parentElement.appendChild(line);

        const content = document.createElement('div');
        content.className = 'page2_content_about';

        const p1 = document.createElement('p');
        p1.innerHTML = `<strong>${subTitle1}</strong>`;
        const p2 = document.createElement('p');
        p2.textContent = text1;
        const p3 = document.createElement('p');
        p3.innerHTML = `<strong>${subTitle2}</strong>`;
        const p4 = document.createElement('p');
        p4.textContent = text2;

        content.appendChild(p1);
        content.appendChild(p2);
        content.appendChild(p3);
        content.appendChild(p4);
        parentElement.appendChild(content);
    }

    function createMethodologyContent(parentElement) {
        const title = document.createElement('h1');
        title.className = 'page2_content_title_about';
        title.textContent = 'Methodology and approach';
        parentElement.appendChild(title);

        const line = document.createElement('div');
        line.className = 'line';
        parentElement.appendChild(line);

        const content = document.createElement('div');
        content.className = 'page2_content_about';

        const p1 = document.createElement('p');
        p1.textContent = 'We decided to develop our model using a multi-agent system. This approach divides complex tasks into sub-tasks managed by specialized agents, each with distinct roles.';
        content.appendChild(p1);

        const subTitle = document.createElement('p');
        subTitle.className = 'section-title';
        subTitle.textContent = 'Multi-agent system components';
        content.appendChild(subTitle);

        const ul = document.createElement('ul');
        ul.className = 'list';
        const li1 = document.createElement('li');
        li1.innerHTML = '<strong>Agents:</strong> Responsible for specific tasks such as text generation, query management or data analysis.';
        const li2 = document.createElement('li');
        li2.innerHTML = '<strong>Tools:</strong> Specialized modules used by agents to accomplish their tasks, e.g., connecting to and querying the TMDB (The Movie Database).';
        const li3 = document.createElement('li');
        li3.innerHTML = '<strong>Supervisors:</strong> Coordinate agents and tools to ensure smooth communication and efficient query processing.';
        ul.appendChild(li1);
        ul.appendChild(li2);
        ul.appendChild(li3);
        content.appendChild(ul);

        const p2 = document.createElement('p');
        p2.textContent = 'To enrich our model and generate relevant texts, we integrate queries to the TMDB database, which offers a vast collection of information on films, TV series and film personalities.';
        content.appendChild(p2);

        parentElement.appendChild(content);
    }


    // Création du conteneur principal
    const container = document.createElement('div');
    container.className = 'app_container_page';

    // Création de l'en-tête de la page
    const header = document.createElement('div');
    header.className = 'page2_header';

    const logo = document.createElement('img');
    logo.src = 'assets/img/logo.png';
    logo.alt = 'Dell Logo';
    logo.className = 'page2_logo';
    header.appendChild(logo);

    const appName = document.createElement('h1');
    appName.className = 'appName';
    appName.textContent = 'Text AI';
    header.appendChild(appName);

    const linkHeader = document.createElement('div');
    linkHeader.className = 'linkHeader';

    const linkHome = document.createElement('button');
    linkHome.className = 'linkHome';
    linkHome.innerHTML = '<p>Home</p>';
    linkHeader.appendChild(linkHome);

    const linkAbout = document.createElement('button');
    linkAbout.className = 'linkAbout';
    linkAbout.innerHTML = '<p>About</p>';
    linkHeader.appendChild(linkAbout);

    header.appendChild(linkHeader);
    container.appendChild(header);

    // Création de la section About
    const aboutSection = document.createElement('div');
    aboutSection.className = 'page2_about';

    // Contenu About Us
    const aboutContent1 = document.createElement('div');
    aboutContent1.className = 'page2_about_content';
    createAboutContent(aboutContent1, 'About Us', 'Who are we?', 'We\'re Malcom and Cassandra, two students in the MIASHS (Mathématiques et Informatique Appliquées aux Sciences Humaines et Sociales) Licence 3 program at Montpellier\'s Paul Valéry University. Passionate about artificial intelligence and its applications, we decided to devote our internship to an ambitious and innovative project.', 'Our internship topic', 'The subject of our internship is the creation of a generative artificial intelligence for text generation. The aim of this project is to develop a model capable of producing coherent, relevant texts in a variety of contexts. We could use and draw inspiration from several existing models, such as gpt-3 or mistral Ai.');
    aboutSection.appendChild(aboutContent1);

    // Contenu Methodology
    const aboutContent2 = document.createElement('div');
    aboutContent2.className = 'page2_about_content';
    createMethodologyContent(aboutContent2);
    aboutSection.appendChild(aboutContent2);

    container.appendChild(aboutSection);
    document.body.appendChild(container); 

    
    $('.page2_logo').click(function() {
        // Changer de scène
        changeScene(1);
    });
    $('.linkHome').click(function() {
        // Changer de scène
        changeScene(2);
    });
    $('.linkAbout').click(function() {
        // Changer de scène
        changeScene(3);
    });





}
