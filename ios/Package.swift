// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "BlindAI",
    defaultLocalization: "en",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .library(
            name: "BlindAI",
            targets: ["BlindAI"]
        )
    ],
    targets: [
        .target(
            name: "BlindAI",
            path: "BlindAI",
            exclude: [
                "Resources/Info.plist"
            ],
            resources: [
                .process("Resources")
            ]
        )
    ]
)
