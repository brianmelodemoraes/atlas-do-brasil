import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.brexplora.trivia',          // v54: identidade nova (Trivia by Brexplora). Não muda depois de publicado.
  appName: 'Trivia by Brexplora',
  webDir: 'www',
  // O HTML é o mesmo do site (www/index.html). Tiles, base da trivia e Supabase são remotos — o app precisa de rede.
  server: { androidScheme: 'https' },
  ios: { contentInset: 'never', scrollEnabled: false, backgroundColor: '#070A12' },
  android: { backgroundColor: '#070A12', allowMixedContent: false },
  plugins: {
    SplashScreen: { launchShowDuration: 0, launchAutoHide: true, backgroundColor: '#070A12' },
    StatusBar: { style: 'DARK', overlaysWebView: true },            // texto claro sobre o fundo Night
    LocalNotifications: { iconColor: '#4ADE80' },                    // lembrete diário do Impostor (ícone pequeno: padrão; personalizar em res/drawable)
    Keyboard: { resize: 'native', resizeOnFullScreen: true }         // formulário de e-mail (v54) não fica atrás do teclado
  }
};

export default config;
