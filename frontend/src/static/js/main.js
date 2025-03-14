import Alpine from 'alpinejs'
import collapse from '@alpinejs/collapse'
import focus from '@alpinejs/focus'
import mask from '@alpinejs/mask'

import { SidebarState } from './ui'
import { AuthState } from './auth'
import { contentLoader } from './content-loader'

import { createIcons, icons } from 'lucide';

// Variables 
const apiBaseUrl = 'http://localhost:9090/api/v1/';

//Alpine plugins
Alpine.plugin(mask)
Alpine.plugin(focus)
Alpine.plugin(collapse)
 
// Icons
// Caution, this will import all the icons and bundle them.
createIcons({ icons });


// Alpine globals
Alpine.store('ui', {
    ...SidebarState(), 
    ...contentLoader()
});


Alpine.store('auth', {
    ...AuthState(apiBaseUrl)
})




window.Alpine = Alpine
Alpine.start()

