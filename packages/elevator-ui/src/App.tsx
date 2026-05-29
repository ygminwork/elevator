import { AppContainer } from "./app/containers/AppContainer";
import { ElevatorSimulator } from "./elevator/containers/ElevatorSimulator";
import { ElevatorSimulatorThemeProvider } from "./elevator/providers/ElevatorSimulatorThemeProvider";

const App = () => {
  return (
    <AppContainer>
      <ElevatorSimulatorThemeProvider>
        <ElevatorSimulator />
      </ElevatorSimulatorThemeProvider>
    </AppContainer>
  );
};

export default App;
