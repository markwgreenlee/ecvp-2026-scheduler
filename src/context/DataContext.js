import React, { createContext, useState, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import ecvpData from '../../assets/ecvp-data.json';

export const DataContext = createContext();

// Saved schedules hold whole session objects, so they keep whatever the
// programme said on the day they were saved. Re-resolve each one against the
// current data: by id, else by title + day, which survives the poster board
// renumbering (P1.58 -> M1AM8) and picks up corrected abstracts and times.
// Anything that no longer exists in the programme is dropped.
const reconcileSaved = (saved, sessions) => {
  const byId = new Map(sessions.map(s => [s.id, s]));
  const byTitle = new Map(
    sessions.map(s => [`${s.day}|${(s.title || '').toLowerCase()}`, s])
  );
  const seen = new Set();
  const out = [];
  for (const item of saved) {
    const match =
      byId.get(item.id) ||
      byTitle.get(`${item.day}|${(item.title || '').toLowerCase()}`);
    if (match && !seen.has(match.id)) {
      seen.add(match.id);
      out.push(match);
    }
  }
  return out;
};

export const DataProvider = ({ children }) => {
  const [allSessions, setAllSessions] = useState([]);
  const [selectedSessions, setSelectedSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load data
  useEffect(() => {
    const loadData = async () => {
      try {
        // Load sessions from embedded JSON
        setAllSessions(ecvpData);
        
        // Load previously selected sessions
        const saved = await AsyncStorage.getItem('selectedSessions');
        if (saved) {
          setSelectedSessions(reconcileSaved(JSON.parse(saved), ecvpData));
        }
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  // Save selected sessions when they change
  useEffect(() => {
    AsyncStorage.setItem('selectedSessions', JSON.stringify(selectedSessions));
  }, [selectedSessions]);

  const toggleSession = useCallback((session) => {
    setSelectedSessions(prev => {
      const exists = prev.some(s => s.id === session.id);
      if (exists) {
        return prev.filter(s => s.id !== session.id);
      } else {
        return [...prev, session];
      }
    });
  }, []);

  const removeSession = useCallback((sessionId) => {
    setSelectedSessions(prev => prev.filter(s => s.id !== sessionId));
  }, []);

  const clearAll = useCallback(() => {
    setSelectedSessions([]);
  }, []);

  const searchSessions = useCallback((query, day = '', kind = '') => {
    let results = allSessions;

    if (query.trim()) {
      const lowerQuery = query.toLowerCase();
      results = results.filter(s =>
        // Board code / talk number, so "M1AM8" finds that poster directly.
        s.id.toLowerCase().includes(lowerQuery) ||
        s.title.toLowerCase().includes(lowerQuery) ||
        s.authors.join(' ').toLowerCase().includes(lowerQuery) ||
        s.abstract.toLowerCase().includes(lowerQuery) ||
        s.session_title.toLowerCase().includes(lowerQuery) ||
        s.affiliations.toLowerCase().includes(lowerQuery) ||
        (s.bio || '').toLowerCase().includes(lowerQuery) ||
        (s.organizer || '').toLowerCase().includes(lowerQuery)
      );
    }

    if (day) {
      results = results.filter(s => s.day === day);
    }

    if (kind) {
      results = results.filter(s => s.kind === kind);
    }

    return results;
  }, [allSessions]);

  return (
    <DataContext.Provider
      value={{
        allSessions,
        selectedSessions,
        isLoading,
        toggleSession,
        removeSession,
        clearAll,
        searchSessions,
      }}
    >
      {children}
    </DataContext.Provider>
  );
};
