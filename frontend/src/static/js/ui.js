export {SidebarState}

function SidebarState() {
    return {
        isSidebarOpen: true, 
        sidebarActiveItem: 'home', //home as default
    
        toggleSidebar() {
            this.isSidebarOpen = !this.isSidebarOpen
        },

        setSidebarActiveItem(item) {
            this.sidebarActiveItem = item
        }
    }
};
