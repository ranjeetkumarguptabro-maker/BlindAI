import SwiftUI
import Combine

@MainActor
public final class ActiveNavigationViewModel: ObservableObject {
    @Published public var instruction: NavigationInstruction = .mock
    @Published public var isShowingDetails: Bool = false
    @Published public var currentWaypoint: Int = 1
    @Published public var totalWaypoints: Int = 4
    
    public var onNavigateToRoute: ((AppRoute) -> Void)?
    
    private let navService = NavigationService.shared
    private let hapticsService = HapticsService.shared
    private var cancellables = Set<AnyCancellable>()
    
    public init(onNavigateToRoute: ((AppRoute) -> Void)? = nil) {
        self.onNavigateToRoute = onNavigateToRoute
        bindNavigationService()
    }
    
    private func bindNavigationService() {
        navService.$currentInstruction
            .receive(on: DispatchQueue.main)
            .sink { [weak self] newInstruction in
                self?.instruction = newInstruction
            }
            .store(in: &cancellables)
            
        navService.$currentWaypointIndex
            .receive(on: DispatchQueue.main)
            .sink { [weak self] index in
                self?.currentWaypoint = index + 1
            }
            .store(in: &cancellables)
            
        navService.$isNavigating
            .receive(on: DispatchQueue.main)
            .sink { [weak self] navigating in
                if !navigating {
                    self?.onNavigateToRoute?(.home)
                }
            }
            .store(in: &cancellables)
    }
    
    public func handleStopRoute() {
        navService.stopRoute()
    }
    
    public func handleShowDetails() {
        hapticsService.selection()
        isShowingDetails.toggle()
    }
    
    public func repeatCurrentInstruction() {
        navService.repeatInstruction()
    }
    
    public func triggerObstacleAlert() {
        hapticsService.warning()
        onNavigateToRoute?(.obstacleAlert)
    }
    
    public func triggerCrosswalkSafety() {
        hapticsService.impact(style: .heavy)
        onNavigateToRoute?(.crosswalkSafety)
    }
}
