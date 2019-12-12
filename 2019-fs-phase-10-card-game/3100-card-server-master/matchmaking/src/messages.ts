/**
 * All the messages send by the matchmaking server. Names are explanatory to
 * their function.
 */

export const VALID_CLIENT_CONFIG = {
  messageType: 'response',
  data: {
    message: 'Valid configuration found. Please wait for connection.',
  },
};

export const GAME_SERVER_DISCONNECTED = {
  messageType: 'error',
  data: {
    errorType: 'GAME_SERVER_DISCONNECTED',
    message: 'Game server disconnected, please queue up again.',
  },
};

export const VALID_SERVER_CONFIG = {
  messageType: 'response',
  data: {
    message: 'Valid configuration found. Please wait for connection(s).',
  },
};

export const NO_SERVERS_EXIST = {
  messageType: 'error',
  data: {
    errorType: 'NO_SERVERS_EXIST',
    message: 'No servers are currently available for your game.',
  },
};

export const INVALID_CONFIG = {
  messageType: 'error',
  data: {
    errorType: 'INVALID_CONFIG',
    message: 'Invalid configuration.',
  },
};

export const MATCH_FOUND = {
  messageType: 'connect',
  data: {
    message: 'Match Found!',
  },
};

export const KICK_MESSAGE = {
  messageType: 'kick',
  data: {
    message: 'You were kicked from the lobby.',
  },
};

export const CLIENT_DISCONNETED = {
  messageType: 'error',
  data: {
    errorType: 'CLIENT_DISCONNECTED',
    message: 'Client disconnected',
  },
};
