package com.dadm.iceibank.util;

public class RelogioLamport {
    private int contador = 0;

    public synchronized int eventoLocal() {
        contador += 1;
        return contador;
    }

    public synchronized int aoEnviar() {
        contador += 1;
        return contador;
    }

    public synchronized int aoReceber(int timeStampRecebido) {
        contador = Math.max(contador, timeStampRecebido) + 1;
        return contador;
    }
}
