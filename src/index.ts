export function start() {
    const args = process.argv.slice(2);
    console.log("Received command-line arguments:", args);
}
  
start();
