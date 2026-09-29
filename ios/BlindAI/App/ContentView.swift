import SwiftUI

public struct ContentView: View {
    @State private var currentRoute: AppRoute = .home
    
    // ViewModels
    @StateObject private var homeViewModel = HomeViewModel()
    @StateObject private var listeningViewModel = ListeningViewModel()
    @StateObject private var destinationSearchViewModel = DestinationSearchViewModel()
    @StateObject private var routePreviewViewModel = RoutePreviewViewModel()
    @StateObject private var activeNavViewModel = ActiveNavigationViewModel()
    @StateObject private var whereAmIViewModel = WhereAmIViewModel()
    @StateObject private var describeAroundViewModel = DescribeAroundViewModel()
    @StateObject private var obstacleAlertViewModel = ObstacleAlertViewModel()
    @StateObject private var crosswalkSafetyViewModel = CrosswalkSafetyViewModel()
    
    public init() {}
    
    public var body: some View {
        ZStack {
            Color.blindAIBackground
                .ignoresSafeArea()
            
            switch currentRoute {
            case .home:
                HomeView(viewModel: homeViewModel)
                    .transition(.opacity.combined(with: .scale(scale: 0.98)))
                
            case .listening:
                ListeningView(viewModel: listeningViewModel)
                    .transition(.opacity.combined(with: .scale(scale: 1.02)))
                
            case .destinationSearch:
                DestinationSearchView(viewModel: destinationSearchViewModel)
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
                
            case .routePreview:
                RoutePreviewView(viewModel: routePreviewViewModel)
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
                
            case .activeNavigation:
                ActiveNavigationView(viewModel: activeNavViewModel)
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
                
            case .whereAmI:
                WhereAmIView(viewModel: whereAmIViewModel)
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
                
            case .describeAround:
                DescribeAroundView(viewModel: describeAroundViewModel)
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
                
            case .obstacleAlert:
                ObstacleAlertView(viewModel: obstacleAlertViewModel)
                    .transition(.asymmetric(
                        insertion: .move(edge: .bottom).combined(with: .opacity),
                        removal: .move(edge: .top).combined(with: .opacity)
                    ))
                
            case .crosswalkSafety:
                CrosswalkSafetyView(viewModel: crosswalkSafetyViewModel)
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
            }
        }
        .animation(.spring(response: 0.35, dampingFraction: 0.85), value: currentRoute)
        .onAppear {
            configureNavigationCallbacks()
        }
    }
    
    private func configureNavigationCallbacks() {
        homeViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
        
        listeningViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
        
        destinationSearchViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
        
        destinationSearchViewModel.onSelectDestination = { destination in
            self.routePreviewViewModel.destination = destination
        }
        
        routePreviewViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
        
        activeNavViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
        
        whereAmIViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
        
        describeAroundViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
        
        obstacleAlertViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
        
        crosswalkSafetyViewModel.onNavigateToRoute = { route in
            withAnimation { self.currentRoute = route }
        }
    }
}

#Preview {
    ContentView()
}
