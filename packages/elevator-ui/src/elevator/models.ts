export type SimulatorThemeModel = {
  elevator: {
    color: string;
    opacity: number;
    size: number;
  };

  floor: {
    color: string;
    height: number;
    opacity: number;
    padding: number;
  };

  spacing: number;
};

export type PassengerModel = {
  id: string;
};

export type PassengerRequestModel = {
  id: string;
  passenger_id: string;
  pickup: number;
  dropoff: number;
  time_request: number;
  time_pickup?: number;
  time_dropoff?: number;
  elevator_id?: string;
};

export type DispatcherOutputModel = {
  floors: number;

  requests: Array<PassengerRequestModel>;

  passengers: Array<PassengerModel>;

  timestamps: Array<{
    time: number;
    elevators: Array<{
      capacity: number;
      id: string;
      floor: number;
      direction: string;
      pickup_ids: Record<number, Array<string>>;
      dropoff_ids: Record<number, Array<string>>;
      pickups?: Record<number, Array<PassengerRequestModel>>;
      dropoffs?: Record<number, Array<PassengerRequestModel>>;
    }>;
  }>;
};
