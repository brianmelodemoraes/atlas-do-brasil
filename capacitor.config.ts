import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.brexplora.atlas',
  appName: 'Atlas do Brasil',
  webDir: 'www',
  // O HTML é o mesmo do site (www/index.html). Tiles, índice e Supabase são remotos — o app precisa de rede.
  server: { androidScheme: 'https' },
  ios: { contentInset: 'never', scrollEnabled: false, backgroundColor: '#EBDFC2' },
  android: { backgroundColor: '#EBDFC2', allowMixedContent: false },
  plugins: {
    SplashScreen: { launchShowDuration: 0, launchAutoHide: true, backgroundColor: '#EBDFC2' },
    StatusBar: { style: 'LIGHT', overlaysWebView: true }
  }
};

export default config;
