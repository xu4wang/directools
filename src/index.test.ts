import { start } from "./index";

test("start function should handle command-line arguments", () => {
  const consoleSpy = jest.spyOn(console, "log");
  start();
  expect(consoleSpy).toHaveBeenCalledWith("Received command-line arguments:", []);
});
