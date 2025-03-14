import { createIcons, icons } from 'lucide';


export function contentLoader() {
    return {
        content: '',
        isContentLoading: false,


        async loadContent(pagechunk_name) {
            
            let attempts = 3;
            this.content = '';

            //analisar o pagechunk name, atualizar a breadcrumb e a sidebar ou tabs de acordo.

            while (attempts > 0) {
                try {
                    const response = await fetch(pagechunk_name);
                    if (!response.ok) {
                        throw new Error(response.status, response.statusText);
                    }

                    
                    this.content = await response.text();
                    await Alpine.nextTick();
                    this.isContentLoading = false;
                    createIcons({ icons });
                

                    return;
                } catch (error) {
                    attempts--;
                    this.isContentLoading = true;

                    if (attempts === 0) { 
                        this.isContentLoading = false;
                        console.error(error)
                    } else {
                        console.warn(`Erro ao carregar conteúdo: ${error} tries: ${attempts}`);
                        await new Promise(resolve => setTimeout(resolve, 1000)); // Espera antes de tentar novamente
                    }
                }
            }

        }
    };
}