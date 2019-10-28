
const electron = require('electron')
const app = electron.app;
const BrowserWindow = electron.BrowserWindow; 
const path = require("path");
const url = require("url");
const globalShortcut = electron.globalShortcut;

var win; 

function  createWindow(){
    

    win=new BrowserWindow({
        width:1080,
        height: 720,
        icon: path.join(__dirname, 'images/logo.png')});
        win.setMenu(null);
        win.loadURL(url.format({
        pathname: path.join(__dirname,'index.html'),
        protocol: 'file',
        slashes: true
    }));

    win.webContents.openDevTools();
   
    win.on('closed', () => { 
        win=null
    })

    win.maximize();
    win.setResizable(false);
    win.show();

    globalShortcut.register('f5', function() {
		console.log('f5 is pressed')
		win.reload()
  })
  
}

app.on('ready',createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
})