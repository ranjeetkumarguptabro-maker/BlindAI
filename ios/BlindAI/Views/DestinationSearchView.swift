import SwiftUI

public struct DestinationSearchView: View {
    @ObservedObject public var viewModel: DestinationSearchViewModel
    
    public init(viewModel: DestinationSearchViewModel) {
        self.viewModel = viewModel
    }
    
    public var body: some View {
        ZStack(alignment: .bottom) {
            Color.blindAIBackground
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Header with Back button and Settings
                HStack {
                    Button {
                        viewModel.handleBack()
                    } label: {
                        ZStack {
                            Circle()
                                .fill(Color(red: 236/255, green: 236/255, blue: 238/255))
                                .frame(width: 38, height: 38)
                            Image(systemName: "arrow.left")
                                .font(.system(size: 16, weight: .semibold))
                                .foregroundColor(.black)
                        }
                    }
                    .accessibilityLabel("Back to home")
                    
                    Spacer()
                    
                    Text("Blind AI")
                        .font(.blindAIHeaderTitle)
                        .foregroundColor(.blindAITextPrimary)
                    
                    Spacer()
                    
                    Button {} label: {
                        ZStack {
                            Circle()
                                .fill(Color(red: 236/255, green: 236/255, blue: 238/255))
                                .frame(width: 38, height: 38)
                            Image(systemName: "gearshape.fill")
                                .font(.system(size: 16, weight: .semibold))
                                .foregroundColor(.black)
                        }
                    }
                    .accessibilityLabel("Settings")
                }
                .padding(.horizontal, BlindAISpacing.screenPadding)
                .padding(.top, 10)
                .padding(.bottom, 6)
                
                ScrollView(.vertical, showsIndicators: false) {
                    VStack(alignment: .leading, spacing: 18) {
                        // Title
                        Text("Where would you\nlike to go?")
                            .font(.system(size: 28, weight: .bold))
                            .foregroundColor(.black)
                            .lineSpacing(2)
                            .padding(.top, 6)
                            .accessibilityAddTraits(.isHeader)
                        
                        // Search bar
                        HStack(spacing: 10) {
                            Image(systemName: "magnifyingglass")
                                .font(.system(size: 18, weight: .medium))
                                .foregroundColor(.neutral400)
                            
                            TextField("Search for a place or address in Riga", text: $viewModel.searchQuery)
                                .font(.system(size: 15))
                                .foregroundColor(.black)
                        }
                        .padding(.horizontal, 16)
                        .padding(.vertical, 14)
                        .background(Color.white)
                        .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
                        .overlay(
                            RoundedRectangle(cornerRadius: 18, style: .continuous)
                                .stroke(Color.black.opacity(0.04), lineWidth: 1)
                        )
                        .shadow(color: Color.black.opacity(0.03), radius: 6, x: 0, y: 2)
                        
                        // Recent places section
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Recent places")
                                .font(.system(size: 13, weight: .medium))
                                .foregroundColor(.neutral500)
                            
                            VStack(spacing: 8) {
                                ForEach(viewModel.displayedPlaces) { item in
                                    Button {
                                        viewModel.selectDestination(item)
                                    } label: {
                                        HStack(spacing: 14) {
                                            ZStack {
                                                RoundedRectangle(cornerRadius: 12, style: .continuous)
                                                    .fill(item.iconBackground)
                                                    .frame(width: 44, height: 44)
                                                
                                                Image(systemName: item.iconName)
                                                    .font(.system(size: 18, weight: .semibold))
                                                    .foregroundColor(item.iconColor)
                                            }
                                            
                                            VStack(alignment: .leading, spacing: 2) {
                                                Text(item.title)
                                                    .font(.system(size: 16, weight: .semibold))
                                                    .foregroundColor(.black)
                                                    .lineLimit(1)
                                                
                                                Text(item.subtitle)
                                                    .font(.system(size: 13))
                                                    .foregroundColor(.neutral500)
                                                    .lineLimit(1)
                                            }
                                            
                                            Spacer()
                                            
                                            Image(systemName: "chevron.right")
                                                .font(.system(size: 14, weight: .semibold))
                                                .foregroundColor(Color(red: 200/255, green: 200/255, blue: 202/255))
                                        }
                                        .padding(.horizontal, 14)
                                        .padding(.vertical, 10)
                                        .background(Color.white)
                                        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                                        .overlay(
                                            RoundedRectangle(cornerRadius: 16, style: .continuous)
                                                .stroke(Color.black.opacity(0.04), lineWidth: 1)
                                        )
                                    }
                                    .buttonStyle(.plain)
                                }
                            }
                        }
                        
                        // Nearby places section
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Nearby places")
                                .font(.system(size: 13, weight: .medium))
                                .foregroundColor(.neutral500)
                            
                            VStack(spacing: 8) {
                                ForEach(viewModel.nearbyCategories) { cat in
                                    Button {
                                        viewModel.searchQuery = cat.title
                                    } label: {
                                        HStack(spacing: 14) {
                                            ZStack {
                                                RoundedRectangle(cornerRadius: 12, style: .continuous)
                                                    .fill(cat.iconBackground)
                                                    .frame(width: 44, height: 44)
                                                
                                                Image(systemName: cat.iconName)
                                                    .font(.system(size: 18, weight: .semibold))
                                                    .foregroundColor(cat.iconColor)
                                            }
                                            
                                            Text(cat.title)
                                                .font(.system(size: 16, weight: .semibold))
                                                .foregroundColor(.black)
                                            
                                            Spacer()
                                            
                                            Image(systemName: "chevron.right")
                                                .font(.system(size: 14, weight: .semibold))
                                                .foregroundColor(Color(red: 200/255, green: 200/255, blue: 202/255))
                                        }
                                        .padding(.horizontal, 14)
                                        .padding(.vertical, 10)
                                        .background(Color.white)
                                        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                                        .overlay(
                                            RoundedRectangle(cornerRadius: 16, style: .continuous)
                                                .stroke(Color.black.opacity(0.04), lineWidth: 1)
                                        )
                                    }
                                    .buttonStyle(.plain)
                                }
                            }
                        }
                        
                        Spacer(minLength: 80)
                    }
                    .padding(.horizontal, BlindAISpacing.screenPadding)
                }
            }
            
            // Bottom Action Bar: Speak Destination button + Speaker button
            HStack(spacing: 12) {
                Button {
                    viewModel.handleSpeakDestination()
                } label: {
                    HStack(spacing: 10) {
                        Image(systemName: "mic.fill")
                            .font(.system(size: 18, weight: .semibold))
                        Text("Speak destination")
                            .font(.system(size: 16, weight: .semibold))
                    }
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .frame(height: 54)
                    .background(Color.black)
                    .clipShape(Capsule())
                    .shadow(color: Color.black.opacity(0.12), radius: 8, x: 0, y: 3)
                }
                
                SpeakerButton(textToRepeat: "Where would you like to go? You can search for a place in Riga, choose Riga Technical University, or tap speak destination.")
            }
            .padding(.horizontal, BlindAISpacing.screenPadding)
            .padding(.bottom, 20)
        }
    }
}
