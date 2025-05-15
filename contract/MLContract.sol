// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MLContract {
    bool public lastPrediction;   // almacena el último resultado de predicción recibido

    // Evento que se emite cada vez que se actualiza el estado con una nueva predicción
    event PredictionUpdated(bool prediccion);
    // Evento que se emite cuando se ejecuta una acción tras una predicción positiva
    event ActionExecuted();

    // Actualiza el estado almacenando la predicción recibida
    function actualizarEstado(bool _prediccion) public {
        lastPrediction = _prediccion;
        emit PredictionUpdated(_prediccion);
    }

    // Realiza una acción si la última predicción es true.
    // En este ejemplo, simplemente emite un evento para indicar la acción.
    function actuar() public {
        if (lastPrediction) {
            // Tomar acción (ej. emitir un evento, transferir fondos, etc.)
            emit ActionExecuted();
            // Nota: Podría agregarse lógica adicional aquí en un caso real.
        }
        // Si lastPrediction es false, la función no hace nada (no emite evento).
    }
}
