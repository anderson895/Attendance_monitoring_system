<?php
/**
 * Front Controller — every request enters here.
 * URLs follow: index.php?url=controller/action/param
 * (Apache rewrites pretty URLs to this via .htaccess)
 */
require_once 'app/config/config.php';
require_once 'app/core/App.php';

new App();
