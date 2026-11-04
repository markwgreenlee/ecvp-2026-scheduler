import React, { useState, useEffect } from 'react';

// Register service worker for PWA offline support (web only)
if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
  let registration = null;
  let lastCheck = 0;
  // A resume costs one conditional request at most once a minute, which is
  // nothing next to being stuck on a stale programme at the venue.
  const CHECK_INTERVAL_MS = 60000;

  const checkForUpdate = () => {
    if (!registration) return;
    const now = Date.now();
    if (now - lastCheck < CHECK_INTERVAL_MS) return;
    lastCheck = now;
    registration.update().catch(() => {});
  };

  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/ecvp-2026-scheduler/sw.js', { scope: '/ecvp-2026-scheduler/' })
      .then((reg) => {
        registration = reg;
        lastCheck = Date.now();
      })
      .catch(() => {});
  });

  if (typeof document !== 'undefined') {
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') checkForUpdate();
    });
  }
  window.addEventListener('focus', checkForUpdate);
}

// Analytics: none configured. To enable privacy-friendly, cookie-free Umami
// analytics on the web build, inject the script tag here with your own
// data-website-id (see the IMRF/VSS schedulers for the pattern).

import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { ActivityIndicator, View } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';

import HomeScreen from './src/screens/HomeScreen';
import ProgramScreen from './src/screens/ProgramScreen';
import VenueScreen from './src/screens/VenueScreen';
import SearchScreen from './src/screens/SearchScreen';
import ScheduleScreen from './src/screens/ScheduleScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import { DataProvider } from './src/context/DataContext';
import InstallPrompt from './src/components/InstallPrompt';
import ImportPrompt from './src/components/ImportPrompt';
import StartingSoon from './src/components/StartingSoon';
import UpdatePrompt from './src/components/UpdatePrompt';

const Tab = createBottomTabNavigator();

const LoadingScreen = () => (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' }}>
    <ActivityIndicator size="large" color="#16324f" />
  </View>
);

export default function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate data loading
    setTimeout(() => setIsLoading(false), 1000);
  }, []);

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <DataProvider>
        <InstallPrompt />
        <ImportPrompt />
        <StartingSoon />
        <UpdatePrompt />
        <NavigationContainer>
          <Tab.Navigator
            initialRouteName="Home"
            screenOptions={({ route }) => ({
              tabBarIcon: ({ color, size }) => {
                let iconName;
                if (route.name === 'Home') iconName = 'home-outline';
                else if (route.name === 'Program') iconName = 'menu';
                else if (route.name === 'Search') iconName = 'magnify';
                else if (route.name === 'Schedule') iconName = 'star-outline';
                else if (route.name === 'Settings') iconName = 'cog';
                return <Icon name={iconName} size={size} color={color} />;
              },
              tabBarActiveTintColor: '#16324f',
              tabBarInactiveTintColor: '#555',
              headerShown: true,
              headerStyle: {
                backgroundColor: '#16324f',
              },
              headerTintColor: '#fff',
              headerTitleStyle: {
                fontWeight: '600',
              },
            })}
          >
            <Tab.Screen
              name="Home"
              component={HomeScreen}
              options={{
                headerShown: false,
                tabBarLabel: 'Home',
              }}
            />
            <Tab.Screen
              name="Program"
              component={ProgramScreen}
              options={{
                title: 'Program',
                tabBarLabel: 'Program',
              }}
            />
            <Tab.Screen
              name="Search"
              component={SearchScreen}
              options={{
                title: 'Search Presentations',
                tabBarLabel: 'Search',
              }}
            />
            <Tab.Screen
              name="Schedule"
              component={ScheduleScreen}
              options={{
                title: 'My Schedule',
                tabBarLabel: 'Schedule',
              }}
            />
            <Tab.Screen
              name="Settings"
              component={SettingsScreen}
              options={{
                title: 'Settings',
                tabBarLabel: 'Settings',
              }}
            />
            {/* Reached from Home rather than the tab bar, which holds five
                tabs already. Registering it here is what lets Home navigate
                to it without adding a second navigator. */}
            <Tab.Screen
              name="Venue"
              component={VenueScreen}
              options={{
                title: 'Venue Map',
                tabBarButton: () => null,
                tabBarItemStyle: { display: 'none' },
              }}
            />
          </Tab.Navigator>
        </NavigationContainer>
      </DataProvider>
    </GestureHandlerRootView>
  );
}
